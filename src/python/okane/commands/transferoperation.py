from okane.args import ARGS, bcolors


def get_cmd_flags():
    return ["-t", "--transfer"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -t: transference between accounts\n"
    help_usage_str += f"\t{application_cmd} --transfer transference between accounts\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) < 3:
        return

    amount = float(args[0])
    account_names = args[1:len(args)]
    previous_account = None

    for i in range(len(account_names)):
        account_name = account_names[i]
        account_result = controller.get_account_from({ARGS.account: [account_name]})

        if not account_result[0]:
            return

        account = account_result[1]

        if previous_account is not None:
            # Transfer from previous account to the current account
            moneyArgs = {
                'register_dt': controller.get_datetime_from(extra_args)[1],
                'category': controller.get_category_from({ARGS.category: ["Transfer"]})[1],
                'account': previous_account,
                'amount': -amount,
                'description': f"Transferido para a conta '{account.name}'"
            }
            moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
            controller.moneyDAO.save(moneyRegister)

            moneyArgs = {
                'register_dt': controller.get_datetime_from(extra_args)[1],
                'category': controller.get_category_from({ARGS.category: ["Transfer"]})[1],
                'account': account,
                'amount': amount,
                'description': f"Transferido da conta '{previous_account.name}'"
            }
            moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
            controller.moneyDAO.save(moneyRegister)

        previous_account = account
