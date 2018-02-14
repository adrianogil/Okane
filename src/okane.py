#!/usr/bin/env python
import sys, sqlite3, os, datetime
from dateutil.parser import parse as dtparse

import utils, importutils

importutils.addpath(__file__, 'dao')
from dao.moneyregisterdao import MoneyRegisterDAO
importutils.addpath(__file__, 'entity')
from entity.entityfactory import EntityFactory


list_args = '--save -s --list -l'

# Open Connection
okane_directory = os.environ['OKANE_DIR'] + '/db/'
conn = sqlite3.connect(okane_directory + 'okane.sqlite');

# Creating cursor
c = conn.cursor()


entityFactory = EntityFactory()
moneyDAO = MoneyRegisterDAO(conn, c, entityFactory)

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
    c.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            id_category INTEGER,
            category_name TEXT,
            PRIMARY KEY (id_category)
        )
    ''')
    moneyDAO.createTables()
    

def save_register(args, extra_args):
    if len(args) == 2:
        moneyArgs = {
            "amount"      : float(args[1]),
            "description" : args[0],
            'register_dt' : datetime.datetime.now()
        }
        moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
        moneyDAO.save(moneyRegister)

def show_registers(args, extra_args):
    if len(args) == 0:
        register_list = moneyDAO.getAll()
        for money in register_list:
            row_data = (money.id, money.register_dt, money.amount, money.description)
            row_text = bcolors.OKBLUE + 'Id:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Date:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Amount:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Description:' + bcolors.ENDC + ' %s'
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

commands_parse = {
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
    for a in args:
        if a in commands_parse:
            commands_parse[a](args[a], args)

create_tables()
args = parse_arguments()
parse_commands(args)
