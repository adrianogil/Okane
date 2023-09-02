from okane.args import ARGS, bcolors


def get_cmd_flags():
    return ["-ba", "--balance-account"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -ba: show balance per account\n"
    help_usage_str += f"\t{application_cmd} --balance-account: show balance per account\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 0:
        account_list = controller.accountDAO.getAll()
        register_list = controller.moneyDAO.getAll(extra_args)

        income = {}
        outcome = {}
        balance = {}

        for account in account_list:
            income[account.name] = 0
            outcome[account.name] = 0
            balance[account.name] = 0
        for money in register_list:
            if money.amount >= 0:
                income[money.account.name] = income[money.account.name] + money.amount
            else:
                outcome[money.account.name] = outcome[money.account.name] + (-1) * money.amount
            balance[money.account.name] = balance[money.account.name] + money.amount
        for account in account_list:
            if ARGS.oneline in extra_args:
                balance_data = (account.name, \
                                balance[account.name],\
                                income[account.name], \
                                outcome[account.name],\
                                )
                print('%s\t%10.2f [IN]%10.2f [OUT]%10.2f' % balance_data)
            else:
                print('\nBalance account: %s\n' % (account.name,))
                print('Income: %10.2f' % (income[account.name]))
                print('Outcome: %10.2f' % (outcome[account.name]))
                print('Balance: %10.2f' % (balance[account.name]))
