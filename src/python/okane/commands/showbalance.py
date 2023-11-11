from okane.args import ARGS, bcolors


def get_cmd_flags():
    return ["-b", "--balance"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -b: show balance\n"
    help_usage_str += f"\t{application_cmd} --balance: show balance\n"
    return help_usage_str


def execute(args, extra_args, controller):
    dao_args = extra_args.copy()
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
    register_list = controller.moneyDAO.getAll(dao_args)
    income = 0
    outcome = 0
    balance = 0
    for money in register_list:
        if 'accounts' in dao_args or not money.category.name == 'Transfer':
            if money.amount >= 0:
                income = income + money.amount
            else:
                outcome = outcome + (-1) * money.amount
            balance = balance + money.amount
    print('Income: %10.2f' % (income))
    print('Outcome: %10.2f' % (outcome))
    print('Balance: %10.2f' % (balance))