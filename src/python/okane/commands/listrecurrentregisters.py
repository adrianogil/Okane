# Command to list recurrent registers
from okane.args import ARGS, bcolors

from okane.utils import utils

import json


def get_cmd_flags():
    return ["-lr", "--list-recurrent"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -lr: list all recurrent registers\n"
    help_usage_str += f"\t{application_cmd} --list-recurrent: list all recurrent registers\n"
    return help_usage_str


def execute(args, extra_args, controller):
    dao_args = extra_args.copy()
    format_args = None
    if '--format' in extra_args or '-f' in extra_args:
        if '--format' in extra_args:
            format_args = extra_args['--format']
        else:
            format_args = extra_args['-f']

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
            category = controller.get_category_from({ARGS.category : [c]})[1]
            category_conditions.append(category)
            category_conditions.extend(controller.categoryDAO.getChildrenCategories(category.id))
        dao_args['categories'] = category_conditions
    if ARGS.account in extra_args:
        account_conditions = []
        for c in extra_args[ARGS.account]:
            account_conditions.append(controller.get_account_from({ARGS.account : [c]})[1])
        dao_args['accounts'] = account_conditions

    if len(args) > 0:
        dao_args['description'] = args[0]

    register_list = controller.recurrentMoneyDAO.getAll(dao_args)


    if ARGS.json_output in extra_args:
        # Print output as json
        money_data_list = []
        for money in register_list:
            money_data_list.append(money.get_data())
        list_data = {
            'list': money_data_list
        }
        print(json.dumps(list_data, indent=4))
    else:
        # Print output as text
        for money in register_list:
            row_text =  '(%s) ' + \
                        '[%s] ' + \
                        ' %7.2f: ' + \
                        '%s: ' + \
                        '[Cat] %s ' + \
                        '[Acc] %s '
            row_data = (money.id, \
                    money.start_dt.strftime("%Y.%m.%d"), \
                    money.amount, \
                    money.description, \
                    money.category.name,\
                    money.account.name)
            print(row_text % row_data )
        print(f"Total: {len(register_list)} recurrent registers found", bcolors.OKGREEN)
