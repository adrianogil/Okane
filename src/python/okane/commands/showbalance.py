from okane.args import ARGS, bcolors


def get_cmd_flags():
    return ["-b", "--balance"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -b: show balance\n"
    help_usage_str += f"\t{application_cmd} --balance: show balance\n"
    return help_usage_str


def execute(args, extra_args, controller):
    register_list = controller.moneyDAO.getAll(extra_args)
    income = 0
    outcome = 0
    balance = 0
    for money in register_list:
        if not money.category.name == 'Transfer':
            if money.amount >= 0:
                income = income + money.amount
            else:
                outcome = outcome + (-1) * money.amount
            balance = balance + money.amount
    print('Income: %10.2f' % (income))
    print('Outcome: %10.2f' % (outcome))
    print('Balance: %10.2f' % (balance))