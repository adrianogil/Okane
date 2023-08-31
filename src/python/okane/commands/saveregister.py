from okane.utils import utils


def get_cmd_flags():
    return ["-s", "--save"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -s <description> <amount> -dt <date> -cs <category> -ac <account>: save a register\n"
    help_usage_str += f"\t{application_cmd} --save <description> <amount> -dt <date> -cs <category> -ac <account>: save a register\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) >= 2:
        moneyArgs = {
            'register_dt' : controller.get_datetime_from(extra_args)[1],
            'category'    : controller.get_category_from(extra_args)[1],
            'account'     : controller.get_account_from(extra_args)[1],
        }
        for i in range(0, 2):
            if utils.is_float(args[i]):
                moneyArgs['amount'] = float(args[i])
            else:
                moneyArgs['description'] = args[i]
        moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
        controller.moneyDAO.save(moneyRegister)
        if len(args) > 2:
            for i in range(2, len(args)):
                if utils.is_float(args[i]):
                    moneyArgs['amount'] = float(args[i])
                    moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
                    controller.moneyDAO.save(moneyRegister)
    else:
        print("Missing arguments")
        print("Usage: python3 -m okane -s <description> <amount> -dt <date> -cs <category> -ac <account>")
