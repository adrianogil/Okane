#!/usr/bin/env python
import sys, sqlite3, os, datetime
from dateutil.parser import parse as dtparse

import utils, importutils

importutils.addpath(__file__, 'dao')
from dao.moneyregisterdao import MoneyRegisterDAO

list_args = '--save -s --list -l'

# Open Connection
okane_directory = os.environ['OKANE_DIR'] + '/db/'
conn = sqlite3.connect(okane_directory + 'okane.sqlite');

# Creating cursor
c = conn.cursor()

moneyDAO = MoneyRegisterDAO(c)

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
    

def save_register(args):
    if len(args) == 2:
        # Save current register
        sql_query_save = "INSERT INTO FinancialRegisters (description, amount, register_dt)" + \
                        " VALUES (:description,:amount,:register_dt)"
        
        now = datetime.datetime.now()
        save_data = (args[0], float(args[1]), now.strftime("%Y-%m-%d %H:%M:%S")) # YYYY-MM-DD HH:MM:SS.SSS

        c.execute(sql_query_save, save_data)
        conn.commit()
        print '.'

def show_registers(args):
    if len(args) == 0:
        c.execute("SELECT * from FinancialRegisters ORDER BY date(register_dt)")
        for row in c:
            reg_date = str(row[3])
            row_data = (str(row[0]), reg_date, str(row[1]), str(row[2]))
            row_text = bcolors.OKBLUE + 'Id:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Date:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Amount:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Description:' + bcolors.ENDC + ' %s'
            print(row_text % row_data )

def show_balance(args):
    if len(args) == 0:
        c.execute("SELECT * from FinancialRegisters ORDER BY date(register_dt)")
        income = 0
        outcome = 0
        balance = 0
        for row in c:
            amount = float(row[2])
            if amount >= 0:
                income = income + amount
            else:
                outcome = outcome + (-1) * amount
            balance = balance + amount
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
            commands_parse[a](args[a])

create_tables()
args = parse_arguments()
parse_commands(args)
