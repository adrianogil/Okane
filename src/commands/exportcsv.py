import csv

class ARGS:
    account     = '-ac'
    category    = '-cs'
    datetime    = '-dt'
    porcelain   = '--porcelain'
    oneline     = '-oneline'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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