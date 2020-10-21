import csv

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
                'account'     : controller.get_account_from({ARGS.category:[row['Account']]})[1],
                'amount'      : float(row['Amount']),
                'description' : row['Description']
            }
            moneyRegister = entityFactory.createMoneyRegister(moneyArgs)
            controller.moneyDAO.save(moneyRegister)