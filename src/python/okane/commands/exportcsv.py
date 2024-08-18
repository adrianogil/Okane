from okane.args import ARGS

from okane.utils import utils

import csv

def get_cmd_flags():
    return ["-e", "--export-csv"]

def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -e <path-csv-to-be-saved>: export a csv file\n"
    help_usage_str += f"\t{application_cmd} --export-csv <path-csv-to-be-saved>: export a csv file\n"
    return help_usage_str

def execute(args, extra_args, controller):
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
            category_conditions.append(controller.get_category_from({ARGS.category : [c]})[1])
        dao_args['categories'] = category_conditions

    register_list = controller.moneyDAO.getAll(dao_args)

    # Open the file with utf-8 encoding
    with open(filename, 'w', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        fields_names = [
            'MoneyId',
            'Date',
            'Amount',
            'Description',
            'Category',
            'Account',
            'Confirmed',
            'RecurrentRegisterId'
        ]
        writer.writerow([str(s) for s in fields_names])
        for money in register_list:
            row_data = [
                money.id,
                money.register_dt,
                money.amount,
                money.description,
                money.category.name,
                money.account.name,
                money.confirmed,
                money.recurrent_register.id if money.recurrent_register else None
            ]
            writer.writerow([str(s) for s in row_data])
