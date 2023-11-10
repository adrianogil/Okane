from okane.args import ARGS, bcolors

import csv


def get_cmd_flags():
    return ["-csv", "--import-csv"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -csv <path-csv-to-be-loaded>: import a csv file\n"
    help_usage_str += f"\t{application_cmd} --import-csv <path-csv-to-be-loaded>: import a csv file\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) > 0:
        filename = args[0]
    else:
        filename = 'data.csv'

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row['MoneyId'], row['Amount'], row['Date'])
            moneyArgs = {
                'register_dt' : controller.get_datetime_from({ARGS.datetime:[row['Date']]})[1],
                'category'    : controller.get_category_from({ARGS.category:[row['Category']]})[1],
                'account'     : controller.get_account_from({ARGS.account:[row['Account']]})[1],
                'amount'      : float(row['Amount']),
                'description' : row['Description']
            }
            if "Confirmed" in row:
                moneyArgs["confirmed"] = row["Confirmed"]
            moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
            controller.moneyDAO.save(moneyRegister)
