from okane.args import ARGS, bcolors


def get_cmd_flags():
    return ["-bt", "--balance-time"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -bt: show balance through time\n"
    help_usage_str += f"\t{application_cmd} --balance-time: show balance through time\n"
    return help_usage_str


def execute(args, extra_args, controller):
    dao_args = extra_args.copy()
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
    register_list = controller.moneyDAO.getAll(dao_args)
    
    income_by_date = {}
    outcome_by_date = {}
    balance_by_date = {}

    income = 0
    outcome = 0
    balance = 0

    for money in register_list:
        current_date = money.register_dt.strftime("%Y.%m.%d")
        if 'accounts' in dao_args or not money.category.name == 'Transfer':
            if money.amount >= 0:
                income = income + money.amount
                income_by_date[current_date] = income
            else:
                outcome = outcome + (-1) * money.amount
                outcome_by_date[current_date] = outcome
            balance = balance + money.amount
            balance_by_date[current_date] = balance

    dates = sorted(balance_by_date.keys())

    print('Balance:\n')

    last_income = 0.0
    last_outcome = 0.0

    for date in dates:
        print(f'{date}: %.2f (I: %.2f) (O: %.2f)' % (
            balance_by_date[date], 
            income_by_date[date] if date in income_by_date else last_income, 
            outcome_by_date[date] if date in outcome_by_date else last_outcome ))
        last_income = income_by_date[date] if date in income_by_date else last_income
        last_outcome = outcome_by_date[date] if date in outcome_by_date else last_outcome
