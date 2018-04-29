#!/usr/bin/env python
import sys, sqlite3, os, datetime
from dateutil.parser import parse as dtparse

import utils, importutils

import pandas as pd

import csv

importutils.addpath(__file__, 'dao')
from dao.moneyregisterdao import MoneyRegisterDAO
from dao.categorydao import CategoryDAO
from dao.accountdao import AccountDAO
importutils.addpath(__file__, 'entity')
from entity.entityfactory import EntityFactory

import codecs
import locale

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)


# Open Connection
okane_directory = os.environ['OKANE_DIR'] + '/db/'
conn = sqlite3.connect(okane_directory + 'okane.sqlite');

# Creating cursor
c = conn.cursor()

entityFactory = EntityFactory()
accountDAO = AccountDAO(conn, c, entityFactory)
categoryDAO = CategoryDAO(conn, c, entityFactory)
moneyDAO = MoneyRegisterDAO(conn, c, entityFactory, categoryDAO, accountDAO)

class ARGS:
    account = '-ac'
    category = '-cs'
    datetime = '-dt'
    porcelain = '--porcelain'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_tables():
    # Create table
    accountDAO.createTables()
    categoryDAO.createTables()
    moneyDAO.createTables()

def get_category_from(extra_args):
    if ARGS.category in extra_args and len(extra_args[ARGS.category]) > 0:
        category_name = extra_args[ARGS.category][0]
        # print('DEBUG get_category_from ' + category_name)
        if category_name is not '':
            category = categoryDAO.getCategory(category_name)
            if category is not None and category.id > -1:
                return (True, category)
            else:
                categoryDAO.saveCategory(category_name)
                category = categoryDAO.getCategory(category_name)
                return (True, category)
    return (False, categoryDAO.noCategory)

def get_account_from(extra_args):
    if ARGS.account in extra_args and len(extra_args[ARGS.account]) > 0:
        account_name = extra_args[ARGS.account][0]
        # print('DEBUG get_account_from ' + account_name)
        if account_name is not '':
            account = accountDAO.getAccount(account_name)
            if account is not None and account.id > -1:
                return (True, account)
            else:
                accountDAO.saveAccount(account_name)
                account = accountDAO.getAccount(account_name)
                return (True, account)
    return (False, accountDAO.defaultAccount)

def get_datetime_from(extra_args):
    if ARGS.datetime in extra_args and len(extra_args[ARGS.datetime]) > 0:
        datetime_str = extra_args[ARGS.datetime][0]
        if datetime_str is not '':
            try:
                datetime_value = dtparse(datetime_str)
                return (True, datetime_value)
            except:
                pass
    return (False, datetime.datetime.now())

def save_register(args, extra_args):
    # print('DEBUG: save_register with args: ' + str(args) + ' and extra_args: ' + str(extra_args))
    if len(args) >= 2:
        moneyArgs = {
            'register_dt' : get_datetime_from(extra_args)[1],
            'category'    : get_category_from(extra_args)[1],
            'account'     : get_account_from(extra_args)[1],
        }
        for i in xrange(0, 2):
            if utils.is_float(args[i]):
                moneyArgs['amount'] = float(args[i])
            else:
                moneyArgs['description'] = args[i]
        moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
        moneyDAO.save(moneyRegister)
        if len(args) > 2:
            for i in xrange(2, len(args)):
                if utils.is_float(args[i]):
                    moneyArgs['amount'] = float(args[i])
                    moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
                    moneyDAO.save(moneyRegister)


def delete_register(args, extra_args):
    if len(args) == 1:
        money_id = int(args[0])
        moneyRegister = moneyDAO.getFromId(money_id)
        if moneyRegister is None or moneyRegister.id < 0:
            print("It couldn't find a financial register with given id.")
            return
        moneyDAO.delete(moneyRegister)
        print('Register deleted!')

def update_register(args, extra_args):
    if len(args) >= 1:
        money_id = int(args[0])
        moneyRegister = moneyDAO.getFromId(money_id)
        if moneyRegister is None or moneyRegister.id < 0:
            print("It couldn't find a financial register with given id.")
            return
        for i in xrange(1, len(args)):
            if utils.is_float(args[i]):
                moneyRegister.amount = float(args[i])
            else:
                moneyRegister.description = args[i]
        new_cat = get_category_from(extra_args)
        if new_cat[0]:
            moneyRegister.category = new_cat[1]

        new_dt = get_datetime_from(extra_args)
        if new_dt[0]:
            moneyRegister.register_dt = new_dt[1]
        # print('Trying to update register: ' + str(moneyRegister) )
        moneyDAO.update(moneyRegister)

def show_registers(args, extra_args):
    dao_args = extra_args.copy()

    for a in args:
        if utils.is_int(a):
            number = int(a)
            if number < 0:
                dao_args['limit'] = str((-1) * number)
            else:
                dao_args['offset'] = str(number)

    if ARGS.category in extra_args:
        category_conditions = []
        for c in extra_args[ARGS.category]:
            category_conditions.append(get_category_from({ARGS.category : [c]})[1])
        dao_args['categories'] = category_conditions
    if ARGS.account in extra_args:
        account_conditions = []
        for c in extra_args[ARGS.account]:
            account_conditions.append(get_account_from({ARGS.account : [c]})[1])
        dao_args['accounts'] = account_conditions
    if len(args) > 0:
        dao_args['description'] = args[0]
    register_list = moneyDAO.getAll(dao_args)
    # print('Found %s registers' % (len(register_list),))
    total_amount = 0
    for money in register_list:
        row_data = (money.id, \
                    money.register_dt, \
                    money.amount, \
                    money.description, \
                    money.category.name,\
                    money.account.name)
        total_amount = total_amount + money.amount
        if ARGS.porcelain in extra_args:
            row_text =  '\nId:' +  ' %s\t' + \
                    'Date:' +  ' %s\t' + \
                    'Amount:' +  ' %10.2f\t' + \
                    '\nDescription:' +  ' %s\t' + \
                    '\nCategory:' +  ' %s\t' + \
                    'Account:' +  ' %s'
        else:
            row_text = bcolors.OKBLUE + '\nId:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Date:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Amount:' + bcolors.ENDC + ' %10.2f\t' + \
                       bcolors.OKBLUE + '\nDescription:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + '\nCategory:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Account:' + bcolors.ENDC + ' %s'
        print(row_text % row_data )
    if '--format' in extra_args or '-f' in extra_args:
        if '--format' in extra_args:
            format_args = extra_args['--format']
        else:
            format_args = extra_args['-f']

        if 'b' in format_args:
            print('\nBalance:\t%s' % (total_amount,))



def show_balance(args, extra_args):
    if len(args) == 0:
        register_list = moneyDAO.getAll(extra_args)
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

def show_balance_per_account(args, extra_args):
    if len(args) == 0:
        account_list = accountDAO.getAll()
        register_list = moneyDAO.getAll(extra_args)

        income = {}
        outcome = {}
        balance = {}

        for account in account_list:
            income[account.name] = 0
            outcome[account.name] = 0
            balance[account.name] = 0
        for money in register_list:
            if money.amount >= 0:
                income[money.account.name] = income[money.account.name] + money.amount
            else:
                outcome[money.account.name] = outcome[money.account.name] + (-1) * money.amount
            balance[money.account.name] = balance[money.account.name] + money.amount
        for account in account_list:
            print('\nBalance account: %s\n' % (account.name,))
            print('Income: %10.2f' % (income[account.name]))
            print('Outcome: %10.2f' % (outcome[account.name]))
            print('Balance: %10.2f' % (balance[account.name]))

def show_balance_per_category(args, extra_args):
    if len(args) == 0:
        category_list = categoryDAO.getAll()
        register_list = moneyDAO.getAll(extra_args)

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

def save_category(args, extra_args):
    if len(args) == 1:
        categoryDAO.saveCategory(args[0])


def list_categories(args, extra_args):
    if len(args) == 0:
        category_list = categoryDAO.getAll()
        for category in category_list:
            row_data = (category.id, category.name)
            row_text = bcolors.OKBLUE + 'Id:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Category:' + bcolors.ENDC + ' %s'
            print(row_text % row_data )

def update_category(args, extra_args):
    if len(args) == 2:
        cat_id = int(args[0])
        category = categoryDAO.getCategoryFromId(cat_id)
        if category is None or category.id < 0:
            print("It couldn't find category with the given id: " + str(cat_id))
        category.name = args[1]
        categoryDAO.updateCategory(category)

def delete_category(args, extra_args):
    if len(args) == 1:
        cat_id = int(args[0])
        category = categoryDAO.getCategoryFromId(cat_id)
        if category is None or category.id < 0:
            print("It couldn't find category with the given id: " + str(cat_id))
        categoryDAO.delete(category)

def save_account(args, extra_args):
    if len(args) == 1:
        accountDAO.saveAccount(args[0])

def list_accounts(args, extra_args):
    if len(args) == 0:
        account_list = accountDAO.getAll()
        for account in account_list:
            row_data = (account.id, account.name)
            row_text = bcolors.OKBLUE + 'Id:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Account:' + bcolors.ENDC + ' %s'
            print(row_text % row_data )

def update_account(args, extra_args):
    if len(args) == 2:
        cat_id = int(args[0])
        account = accountDAO.getAccountFromId(cat_id)
        if account is None or account.id < 0:
            print("It couldn't find account with the given id: " + str(cat_id))
        account.name = args[1]
        accountDAO.update(account)

def delete_account(args, extra_args):
    if len(args) == 1:
        if utils.is_int(args[0]):
            cat_id = int(args[0])
            account = accountDAO.getAccountFromId(cat_id)
        else:
            account_name = args[0]
            account = accountDAO.getAccount(account_name)
        if account is None or account.id < 0:
            print("It couldn't find account with the given parameter: " + args[0])
            return

        accountDAO.delete(account)

def transfer_operation(args, extra_args):
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
        moneyDAO.save(moneyRegister)

        moneyArgs = {
            'register_dt' : get_datetime_from(extra_args)[1],
            'category'    : get_category_from({ARGS.category:["Transfer"]})[1],
            'account'     : account2,
            'amount'      : amount,
            'description' : "Transferido da conta '" + account1.name + "'"
        }
        moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
        moneyDAO.save(moneyRegister)



def load_from_xls(args, extra_args):
    if len(args) == 1:
        xls_path = args[0]
        if os.path.isfile(xls_path):
            df = pd.read_excel(xls_path)

            total_registers = len(df)

            keys = df.keys()

            # import pdb; pdb.set_trace() # Start debugger

            for i in xrange(0, total_registers):
                moneyArgs = {
                    'register_dt' : get_datetime_from({ARGS.datetime:[df[keys[0]][i]]})[1],
                    'category'    : get_category_from({ARGS.category:[df[keys[3]][i].strip()]})[1],
                    'account'     : get_account_from({ARGS.category:[df[keys[4]][i].strip()]})[1],
                    'amount'      : float(df[keys[2]][i]),
                    'description' : df[keys[1]][i].strip()
                }
                moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
                moneyDAO.save(moneyRegister)
                # print(k)
                # print(df[k][0].decode('utf-8', 'ignore'))

def export_csv(args, extra_args):
    if len(args) > 0:
        filename = args[0]
    else:
        filename = 'data.csv'

    dao_args = extra_args.copy()

    for a in args:
        if utils.is_int(a):
            number = int(a)
            if number < 0:
                dao_args['limit'] = str((-1) * number)
            else:
                dao_args['offset'] = str(number)

    if ARGS.category in extra_args:
        category_conditions = []
        for c in extra_args[ARGS.category]:
            category_conditions.append(get_category_from({ARGS.category : [c]})[1])
        dao_args['categories'] = category_conditions
    register_list = moneyDAO.getAll(dao_args)

    writer = csv.writer(open(filename, 'w'))
    fields_names = ['MoneyId', \
                    'Date',\
                    'Amount',\
                    'Description',\
                    'Category',\
                    'Account'\
    ]
    writer.writerow([unicode(s).encode("utf-8") for s in fields_names])
    for money in register_list:
        row_data = [money.id, \
                    money.register_dt, \
                    money.amount, \
                    money.description, \
                    money.category.name,\
                    money.account.name]
        writer.writerow([unicode(s).encode("utf-8") for s in row_data])


def import_csv(args, extra_args):
    if len(args) > 0:
        filename = args[0]
    else:
        filename = 'data.csv'

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row['MoneyId'], row['Amount'], row['Date'])
            moneyArgs = {
                'register_dt' : get_datetime_from({ARGS.datetime:[row['Date']]})[1],
                'category'    : get_category_from({ARGS.category:[row['Category']]})[1],
                'account'     : get_account_from({ARGS.category:[row['Account']]})[1],
                'amount'      : float(row['Amount']),
                'description' : row['Description']
            }
            moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
            moneyDAO.save(moneyRegister)



commands_parse = {
    '-csv': import_csv,
    '-xls': load_from_xls,
    '-sa' : save_account,
    '-la' : list_accounts,
    '-ua' : update_account,
    '-da' : delete_account,
    '-lc' : list_categories,
    '-uc' : update_category,
    '-dc' : delete_category,
    '-sc' : save_category,
    '-ba' : show_balance_per_account,
    '-bc' : show_balance_per_category,
    '-t'  : transfer_operation,
    '-s'  : save_register,
    '-l'  : show_registers,
    '-e'  : export_csv,
    '-d'  : delete_register,
    '-u'  : update_register,
    '-b'  : show_balance
}

def parse_arguments():

    args = {}

    last_key = ''

    for i in xrange(1, len(sys.argv)):
        a = sys.argv[i]
        if a[0] == '-' and not utils.is_float(a):
            last_key = a
            args[a] = []
        elif last_key != '':
            arg_values = args[last_key]
            arg_values.append(a)
            args[last_key] = arg_values

    return args

def parse_commands(args):
    # print('DEBUG: Parsing args: ' + str(args))
    for a in args:
        if a in commands_parse:
            commands_parse[a](args[a], args)

create_tables()
args = parse_arguments()
parse_commands(args)

# Load from XLS
# from pandas import DataFrame, read_csv
# import matplotlib.pyplot as plt
# import pandas as pd

# file = r'/Users/gil/Dropbox/Documents/Bank/MinhasEconomias/Extrato_20180101_20180131.xls'
# df = pd.read_excel(file)

# for k in df:
#         print df[k][0]