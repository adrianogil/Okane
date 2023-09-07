from okane.args import ARGS, bcolors


def get_cmd_flags():
    return ["-bc", "--balance-category"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -bc: show balance per category\n"
    help_usage_str += f"\t{application_cmd} --balance-category: show balance per category\n"
    return help_usage_str


def execute(args, extra_args, controller):
    category_list = controller.categoryDAO.getAll()
    register_list = controller.moneyDAO.getAll(extra_args)

    income = {}
    outcome = {}
    balance = {}

    for category in category_list:
        income[category.name] = 0
        outcome[category.name] = 0
        balance[category.name] = 0
    for money in register_list:
        if money.amount >= 0:
            income[money.category.name] = income[money.category.name] + money.amount
        else:
            outcome[money.category.name] = outcome[money.category.name] + (-1) * money.amount
        balance[money.category.name] = balance[money.category.name] + money.amount
    for category in category_list:
        print('\nBalance category: %s\n' % (category.name,))
        print('Income: %10.2f' % (income[category.name]))
        print('Outcome: %10.2f' % (outcome[category.name]))
        print('Balance: %10.2f' % (balance[category.name]))