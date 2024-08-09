from okane.dao.recurrentregisterdao import MoneyRecurrentRegisterDAO
from okane.dao.moneyregisterdao import MoneyRegisterDAO
from okane.dao.categorydao import CategoryDAO
from okane.dao.accountdao import AccountDAO

from okane.entity.entityfactory import EntityFactory

from okane.commands import okanecommands

from okane.utils import utils as utils
from okane.args import ARGS

from .dbcontroller import DbController

from dateutil.parser import parse as dtparse

import datetime


class OkaneController:
    def __init__(self, okane_directory):
        self.db_controller = DbController(okane_directory)

        self.entityFactory = EntityFactory()
        self.accountDAO = AccountDAO(self.db_controller, self.entityFactory)
        self.categoryDAO = CategoryDAO(self.db_controller, self.entityFactory)
        self.moneyDAO = MoneyRegisterDAO(self.db_controller, self.entityFactory, \
                self.categoryDAO, self.accountDAO)
        self.recurrentMoneyDAO = MoneyRecurrentRegisterDAO(self.db_controller, self.entityFactory, \
                self.categoryDAO, self.accountDAO)

    def create_tables(self):
        # Create table
        self.accountDAO.createTables()
        self.categoryDAO.createTables()
        self.moneyDAO.createTables()
        self.recurrentMoneyDAO.createTables()

    def get_category_from(self, extra_args):
        category_value = extra_args
        if isinstance(extra_args, dict):
            if ARGS.category in extra_args and len(extra_args[ARGS.category]) > 0:
                category_value = extra_args[ARGS.category][0]
            else:
                print("No category found")
                exit()
        if category_value != '':
            if utils.is_int(category_value):
                category_id = int(category_value)
                category = self.categoryDAO.getCategoryFromId(category_id)
            else:
                category_name = category_value
                category = self.categoryDAO.getCategory(category_name)
            if category is not None and category.id > -1:
                return (True, category)
            else:
                print("No category found")
                exit()
        return (False, self.categoryDAO.noCategory)

    def get_account_from(self, extra_args):
        account_value = extra_args
        if isinstance(extra_args, dict):
            if ARGS.account in extra_args and len(extra_args[ARGS.account]) > 0:
                account_value = extra_args[ARGS.account][0]
            else:
                print("No account found")
                exit()
        # print('DEBUG get_account_from ' + account_value)
        if account_value != '':
            if utils.is_int(account_value):
                account_id = int(account_value)
                account = self.accountDAO.getAccountFromId(account_id)
                if not account:
                    print("Wrong account id")
                    exit()
            else:
                account_name = account_value
                account = self.accountDAO.getAccount(account_name)
            if account is not None and account.id > -1:
                return (True, account)
            else:
                account_name = account_value
                self.accountDAO.saveAccount(account_name)
                account = self.accountDAO.getAccount(account_name)
                return (True, account)
        return (False, self.accountDAO.defaultAccount)

    def get_datetime_from(self, extra_args):
        datetime_str = extra_args
        if isinstance(extra_args, dict):
            if ARGS.datetime in extra_args and len(extra_args[ARGS.datetime]) > 0:
                datetime_str = extra_args[ARGS.datetime][0]
            else:
                return (False, datetime.datetime.now())

        if datetime_str != '':
            try:
                datetime_value = dtparse(datetime_str)
                return (True, datetime_value)
            except:
                from dategpt import dategpt
                datetime_value  = dategpt.parse_date(datetime_str)
                return (True, datetime_value)
        return (False, datetime.datetime.now())

    def get_register_data_from(self, extra_args):
        moneyArgs = {}
        moneyArgs['register_dt'] = self.get_datetime_from(extra_args)[1]
        moneyArgs['category'] = self.get_category_from(extra_args)[1]
        moneyArgs['account'] = self.get_account_from(extra_args)[1]
        return moneyArgs

    def define_commands(self):
        self.available_commands = okanecommands.get_commands()

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

    def run_cli(self):
        from pyutils.cli.flags import get_parsed_flags
        self.create_tables()
        args = get_parsed_flags()
        self.parse_commands(args)

    def parse_commands(self, args):
        # print('DEBUG: Parsing args: ' + str(args))
        commands_parse = self.get_commands()
        for a in args:
            if a in commands_parse:
                commands_parse[a](args[a], args, self)
                break
