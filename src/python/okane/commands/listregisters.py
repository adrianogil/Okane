from okane.args import ARGS, bcolors
from okane.utils import utils


def get_cmd_flags():
    return ["-l", "--list"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -l: list all registers\n"
    help_usage_str += f"\t{application_cmd} --list: list all registers\n"
    return help_usage_str


def execute(args, extra_args, controller):
    dao_args = extra_args.copy()
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
            category_conditions.append(controller.get_category_from({ARGS.category : [c]})[1])
        dao_args['categories'] = category_conditions
    if ARGS.account in extra_args:
        account_conditions = []
        for c in extra_args[ARGS.account]:
            account_conditions.append(controller.get_account_from({ARGS.account : [c]})[1])
        dao_args['accounts'] = account_conditions
    if len(args) > 0:
        dao_args['description'] = args[0]
    register_list = controller.moneyDAO.getAll(dao_args)
    print('Found %s registers' % (len(register_list),))
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
        elif ARGS.oneline in extra_args:
            row_text =  '(%s) ' + \
                    '[%s] ' + \
                    ' %7.2f: ' + \
                    '%s: ' + \
                    '[Cat] %s ' + \
                    '[Acc] %s '
            row_data = (money.id, \
                    money.register_dt.strftime("%Y-%m-%d"), \
                    money.amount, \
                    money.description, \
                    money.category.name,\
                    money.account.name)
        else:
            row_text = bcolors.OKBLUE + '\nId:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Date:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Amount:' + bcolors.ENDC + ' %10.2f\t' + \
                       bcolors.OKBLUE + '\nDescription:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + '\nCategory:' + bcolors.ENDC + ' %s\t' + \
                       bcolors.OKBLUE + 'Account:' + bcolors.ENDC + ' %s'
        print(row_text % row_data )
        if 'bl' in format_args:
            print('\nBalance:\t%s' % (total_amount,))
    if '--format' in extra_args or '-f' in extra_args:
        if 'b' in format_args:
            print('\nBalance:\t%s' % (total_amount,))