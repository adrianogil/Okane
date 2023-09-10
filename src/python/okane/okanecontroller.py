from okane.dao.moneyregisterdao import MoneyRegisterDAO
from okane.dao.categorydao import CategoryDAO
from okane.dao.accountdao import AccountDAO

from okane.entity.entityfactory import EntityFactory

import okane.commands.updateaccounts as command_updateaccounts
import okane.commands.saveaccounts as command_saveaccounts
import okane.commands.listaccounts as command_listaccounts
import okane.commands.deleteaccount as command_deleteaccount
import okane.commands.listregisters as command_listregisters
import okane.commands.updatecategory as command_updatecategory
import okane.commands.listcategories as command_listcategories
import okane.commands.savecategory as command_savecategory
import okane.commands.deletecategory as command_deletecategory
import okane.commands.saveregister as command_saveregister
import okane.commands.deleteregister as command_deleteregister
import okane.commands.updateregister as command_updateregister
import okane.commands.showbalance as command_showbalance
import okane.commands.showbalanceperaccount as command_showbalanceperaccount
import okane.commands.showbalancepercategory as command_showbalancepercategory
import okane.commands.transferoperation as command_transferoperation
import okane.commands.importcsv as command_importcsv
import okane.commands.exportcsv  as command_exportcsv
import okane.commands.xlsloading as command_xlsloading
import okane.commands.help as command_help

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

    def define_commands(self):
        self.available_commands = [
            command_saveregister,
            command_listregisters,
            command_listaccounts,
            command_saveaccounts,
            command_updateaccounts,
            command_deleteaccount,
            command_updatecategory,
            command_listcategories,
            command_savecategory,
            command_deletecategory,
            command_deleteregister,
            command_updateregister,
            command_showbalance,
            command_showbalanceperaccount,
            command_showbalancepercategory,
            command_transferoperation,
            command_importcsv,
            command_exportcsv,
            command_xlsloading,
            command_help
        ]
    
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
    