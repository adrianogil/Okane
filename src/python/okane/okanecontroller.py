from okane.dao.moneyregisterdao import MoneyRegisterDAO
from okane.dao.categorydao import CategoryDAO
from okane.dao.accountdao import AccountDAO

from okane.entity.entityfactory import EntityFactory

import okane.commands.updateaccounts as command_updateaccounts
import okane.commands.saveaccounts as command_saveaccounts
import okane.commands.listaccounts as command_listaccounts
import okane.commands.deleteaccount as command_deleteaccount
import okane.commands.showregisters as command_showregisters
import okane.commands.updatecategory as command_updatecategory
import okane.commands.listcategories as command_listcategories
import okane.commands.savecategory as command_savecategory
import okane.commands.deletecategory as command_deletecategory
import okane.commands.saveregister as command_saveregister
import okane.commands.deleteregister as command_deleteregister
import okane.commands.showbalanceperaccount as command_showbalanceperaccount
import okane.commands.help as command_help

import okane.commands.importcsv
import okane.commands.exportcsv
import okane.commands.xlsloading

from okane.utils import utils as utils
from okane.args import ARGS, bcolors

from dateutil.parser import parse as dtparse

import sys, sqlite3, os, datetime
import csv
import json


class OkaneController:
    def __init__(self, okane_directory):
        self.okane_directory = okane_directory

        try:
            self.config_path = os.environ["OKANE_CONFIG_PATH"]
        except:
            self.config_path = self.okane_directory + "/../config/okane.config"
        self.load_config()

        db_folder = os.path.dirname(self.db_path)
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
        self.conn = sqlite3.connect(self.db_path)

        # Creating cursor
        self.c = self.conn.cursor()
        self.entityFactory = EntityFactory()
        self.accountDAO = AccountDAO(self.conn, self.c, self.entityFactory)
        self.categoryDAO = CategoryDAO(self.conn, self.c, self.entityFactory)
        self.moneyDAO = MoneyRegisterDAO(self.conn, self.c, self.entityFactory, \
                self.categoryDAO, self.accountDAO)

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
        else:
            config_data = {
                "db_path" : self.okane_directory + "/../db/okane.sqlite"
            }
            # Writing JSON data
            if not os.path.exists(self.okane_directory + "/../config/"):
                os.mkdir(self.okane_directory + "/../config")
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f)

        self.db_path = config_data['db_path']

    def create_tables(self):
        # Create table
        self.accountDAO.createTables()
        self.categoryDAO.createTables()
        self.moneyDAO.createTables()

    def get_category_from(self, extra_args):
        if ARGS.category in extra_args and len(extra_args[ARGS.category]) > 0:
            category_name = extra_args[ARGS.category][0]
            # print('DEBUG get_category_from ' + category_name)
            if category_name != '':
                category = self.categoryDAO.getCategory(category_name)
                if category is not None and category.id > -1:
                    return (True, category)
                else:
                    self.categoryDAO.saveCategory(category_name)
                    category = self.categoryDAO.getCategory(category_name)
                    return (True, category)
        return (False, self.categoryDAO.noCategory)

    def get_account_from(self, extra_args):
        if ARGS.account in extra_args and len(extra_args[ARGS.account]) > 0:
            account_name = extra_args[ARGS.account][0]
            # print('DEBUG get_account_from ' + account_name)
            if account_name != '':
                account = self.accountDAO.getAccount(account_name)
                if account is not None and account.id > -1:
                    return (True, account)
                else:
                    self.accountDAO.saveAccount(account_name)
                    account = self.accountDAO.getAccount(account_name)
                    return (True, account)
        return (False, self.accountDAO.defaultAccount)

    def get_datetime_from(self, extra_args):
        if ARGS.datetime in extra_args and len(extra_args[ARGS.datetime]) > 0:
            datetime_str = extra_args[ARGS.datetime][0]
            if datetime_str != '':
                try:
                    datetime_value = dtparse(datetime_str)
                    return (True, datetime_value)
                except:
                    pass
        return (False, datetime.datetime.now())

    def update_register(self, args, extra_args):
        if len(args) >= 1:
            money_id = int(args[0])
            moneyRegister = self.moneyDAO.getFromId(money_id)
            if moneyRegister is None or moneyRegister.id < 0:
                print("It couldn't find a financial register with given id.")
                return
            for i in range(1, len(args)):
                if utils.is_float(args[i]):
                    moneyRegister.amount = float(args[i])
                else:
                    moneyRegister.description = args[i]
            new_cat = get_category_from(extra_args)
            if new_cat[0]:
                moneyRegister.category = new_cat[1]

            new_account = get_account_from(extra_args)
            if new_account[0]:
                moneyRegister.account = new_account[1]

            new_dt = get_datetime_from(extra_args)
            if new_dt[0]:
                moneyRegister.register_dt = new_dt[1]
            # print('Trying to update register: ' + str(moneyRegister) )
            self.moneyDAO.update(moneyRegister)

    def show_balance(self, args, extra_args):
        if len(args) == 0:
            register_list = self.moneyDAO.getAll(extra_args)
            income = 0
            outcome = 0
            balance = 0
            for money in register_list:
                if not money.category.name == 'Transfer':
                    if money.amount >= 0:
                        income = income + money.amount
                    else:
                        outcome = outcome + (-1) * money.amount
                    balance = balance + money.amount
            print('Income: %10.2f' % (income))
            print('Outcome: %10.2f' % (outcome))
            print('Balance: %10.2f' % (balance))

    def show_balance_per_category(self, args, extra_args):
        if len(args) == 0:
            category_list = self.categoryDAO.getAll()
            register_list = self.moneyDAO.getAll(extra_args)

            income = {}
            outcome = {}
            balance = {}

            for category in category_list:
                income[category.name] = 0
                outcome[category.name] = 0
                balance[category.name] = 0
            for money in register_list:
                if money.amount >= 0:
                    income[money.category.name] = income[money.category.name] + money.amount
                else:
                    outcome[money.category.name] = outcome[money.category.name] + (-1) * money.amount
                balance[money.category.name] = balance[money.category.name] + money.amount
            for category in category_list:
                print('\nBalance category: %s\n' % (category.name,))
                print('Income: %10.2f' % (income[category.name]))
                print('Outcome: %10.2f' % (outcome[category.name]))
                print('Balance: %10.2f' % (balance[category.name]))

    def transfer_operation(self, args, extra_args):
        if len(args) == 3:
            amount = float(args[0])
            account1_name = args[1]
            account2_name = args[2]

            account1_result = get_account_from({ARGS.account : [account1_name]})
            if account1_result[0]:
                account1 = account1_result[1]
            else:
                return
            account2_result = get_account_from({ARGS.account : [account2_name]})
            if account2_result[0]:
                account2 = account2_result[1]
            else:
                return

            moneyArgs = {
                'register_dt' : get_datetime_from(extra_args)[1],
                'category'    : get_category_from({ARGS.category:["Transfer"]})[1],
                'account'     : account1,
                'amount'      : -amount,
                'description' : "Transferido para a conta '" + account2.name + "'"
            }
            moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
            self.moneyDAO.save(moneyRegister)

            moneyArgs = {
                'register_dt' : get_datetime_from(extra_args)[1],
                'category'    : get_category_from({ARGS.category:["Transfer"]})[1],
                'account'     : account2,
                'amount'      : amount,
                'description' : "Transferido da conta '" + account1.name + "'"
            }
            moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
            self.moneyDAO.save(moneyRegister)



    def load_from_xls(self, args, extra_args):
        xlsloading.execute(args, extra_args, self)

    def export_csv(self, args, extra_args):
        exportcsv.execute(args, extra_args, self)

    def import_csv(self, args, extra_args):
        importcsv.execute(args, extra_args, self)

    def define_commands(self):
        self.available_commands = [
            command_saveregister,
            command_showregisters,
            command_listaccounts,
            command_saveaccounts,
            command_updateaccounts,
            command_deleteaccount,
            command_updatecategory,
            command_listcategories,
            command_savecategory,
            command_deletecategory,
            command_deleteregister,
            command_showbalanceperaccount,
            command_help
        ]
    
    # def get_commands(self):
    #     commands_parse = {
    #         '-csv': self.import_csv,
    #         '-xls': self.load_from_xls,
    #         '-bc' : self.show_balance_per_category,
    #         '-t'  : self.transfer_operation,
    #         '-e'  : self.export_csv,
    #         '-u'  : self.update_register,
    #         '-b'  : self.show_balance,
    #     }
    #     return commands_parse
    
    def get_commands(self):
        commands_parse = {
            'no-args'      : self.handle_no_args,
        }
        self.define_commands()

        for cmd in self.available_commands:
            cmd_flags = cmd.get_cmd_flags()
            for flag in cmd_flags:
                commands_parse[flag] = cmd.execute

        return commands_parse

    def handle_no_args(self):
        print("TODO: implement support for no args")
    