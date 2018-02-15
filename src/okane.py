#!/usr/bin/env python
import sys, sqlite3, os, datetime
from dateutil.parser import parse as dtparse

import utils, importutils

importutils.addpath(__file__, 'dao')
from dao.moneyregisterdao import MoneyRegisterDAO
from dao.categorydao import CategoryDAO
importutils.addpath(__file__, 'entity')
from entity.entityfactory import EntityFactory


list_args = '--save -s --list -l'

# Open Connection
okane_directory = os.environ['OKANE_DIR'] + '/db/'
conn = sqlite3.connect(okane_directory + 'okane.sqlite');

# Creating cursor
c = conn.cursor()

entityFactory = EntityFactory()
categoryDAO = CategoryDAO(conn, c, entityFactory)
moneyDAO = MoneyRegisterDAO(conn, c, entityFactory, categoryDAO)

class ARGS:
    category = '-cs'
    datetime = '-dt'

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
    categoryDAO.createTables()
    moneyDAO.createTables()

def get_category_from(extra_args):
    if ARGS.category in extra_args and len(extra_args[ARGS.category]) > 0:
        category_name = extra_args[ARGS.category][0]
        if category_name is not '':
            category = categoryDAO.getCategory(category_name)
            if category is not None and category.id > -1:
                return (True, category)
            else:
                categoryDAO.saveCategory(category_name)
                category = categoryDAO.getCategory(category_name)
                return (True, category)
    return (False, categoryDAO.noCategory)

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
    if len(args) == 2:
        moneyArgs = {
            "amount"      : float(args[1]),
            "description" : args[0],
            'register_dt' : get_datetime_from(extra_args)[1],
            'category'    : get_category_from(extra_args)[1]
        }
        moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
        moneyDAO.save(moneyRegister)

def update_register(args, extra_args):
    money_id = int(args[0])
    moneyRegister = moneyDAO.getFromId(money_id)
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
    moneyDAO.update(moneyRegister)


def show_registers(args, extra_args):
    if len(args) == 0:
        register_list = moneyDAO.getAll()
        # print('Found %s registers' % (len(register_list),))
        for money in register_list:
            row_data = (money.id, money.register_dt, money.amount, money.description, money.category.name)
            row_text = bcolors.OKBLUE + 'Id:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Date:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Amount:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Description:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Categories:' + bcolors.ENDC + ' %s'
            print(row_text % row_data )


def show_balance(args, extra_args):
    if len(args) == 0:
        register_list = moneyDAO.getAll()
        income = 0
        outcome = 0
        balance = 0
        for money in register_list:
            if money.amount >= 0:
                income = income + money.amount
            else:
                outcome = outcome + (-1) * money.amount
            balance = balance + money.amount
        print('Income: %s' % (income))
        print('Outcome: %s' % (outcome))
        print('Balance: %s' % (balance))

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

commands_parse = {
    '-u' : update_register,
    '-uc': update_category,
    '-lc': list_categories,
    '-sc': save_category,
    '-s' : save_register,
    '-l' : show_registers,
    '-b' : show_balance
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
