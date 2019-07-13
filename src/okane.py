#!/usr/bin/env python
import sys, os

import utils

import codecs
import locale

from okanecontroller import OkaneController

# Open Connection
okane_directory = os.environ['OKANE_DIR']
controller = OkaneController(okane_directory)


def parse_arguments():

    args = {}

    last_key = ''

    for i in range(1, len(sys.argv)):
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
    commands_parse = controller.get_commands()
    for a in args:
        if a in commands_parse:
            commands_parse[a](args[a], args)

controller.create_tables()
args = parse_arguments()
parse_commands(args)