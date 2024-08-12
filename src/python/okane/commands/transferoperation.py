from okane.args import ARGS, bcolors


def get_cmd_flags():
    return ["-t", "--transfer"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -t: transference between accounts\n"
    help_usage_str += f"\t{application_cmd} --transfer transference between accounts\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) >= 3:
        amount = float(args[0])
        account1_name = args[1]
        account2_name = args[2]

        account1_result = controller.get_account_from({ARGS.account : [account1_name]})
        if account1_result[0]:
            account1 = account1_result[1]
        else:
            return
        account2_result = controller.get_account_from({ARGS.account : [account2_name]})
        if account2_result[0]:
            account2 = account2_result[1]
        else:
            return

        moneyArgs = {
            'register_dt' : controller.get_datetime_from(extra_args)[1],
            'category'    : controller.get_category_from({ARGS.category:["Transfer"]})[1],
            'account'     : account1,
            'amount'      : -amount,
            'description' : "Transferido para a conta '" + account2.name + "'"
        }
        moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
        controller.moneyDAO.save(moneyRegister)

        moneyArgs = {
            'register_dt' : controller.get_datetime_from(extra_args)[1],
            'category'    : controller.get_category_from({ARGS.category:["Transfer"]})[1],
            'account'     : account2,
            'amount'      : amount,
            'description' : "Transferido da conta '" + account1.name + "'"
        }
        moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
        controller.moneyDAO.save(moneyRegister)

        if len(args) >= 4:
            account3_name = args[3]
            account3_result = controller.get_account_from({ARGS.account : [account3_name]})
            if account3_result[0]:
                account3 = account3_result[1]
            else:
                return

            moneyArgs = {
                'register_dt' : controller.get_datetime_from(extra_args)[1],
                'category'    : controller.get_category_from({ARGS.category:["Transfer"]})[1],
                'account'     : account2,
                'amount'      : -amount,
                'description' : "Transferido para a conta '" + account3.name + "'"
            }
            moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
            controller.moneyDAO.save(moneyRegister)

            moneyArgs = {
                'register_dt' : controller.get_datetime_from(extra_args)[1],
                'category'    : controller.get_category_from({ARGS.category:["Transfer"]})[1],
                'account'     : account3,
                'amount'      : amount,
                'description' : "Transferido da conta '" + account2.name + "'"
        }
        moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
        controller.moneyDAO.save(moneyRegister)

    if len(args) >= 5:
        account4_name = args[4]
        account4_result = controller.get_account_from({ARGS.account : [account4_name]})
        if account4_result[0]:
            account4 = account4_result[1]
        else:
            return

        moneyArgs = {
            'register_dt' : controller.get_datetime_from(extra_args)[1],
            'category'    : controller.get_category_from({ARGS.category:["Transfer"]})[1],
            'account'     : account3,
            'amount'      : -amount,
            'description' : "Transferido para a conta '" + account4.name + "'"
        }
        moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
        controller.moneyDAO.save(moneyRegister)

        moneyArgs = {
            'register_dt' : controller.get_datetime_from(extra_args)[1],
            'category'    : controller.get_category_from({ARGS.category:["Transfer"]})[1],
            'account'     : account4,
            'amount'      : amount,
            'description' : "Transferido da conta '" + account3.name + "'"
        }
        moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
        controller.moneyDAO.save(moneyRegister)
