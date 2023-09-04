from okane.utils import utils


def get_cmd_flags():
    return ["-u", "--update"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -u <id of existent register>: update an register\n"
    help_usage_str += f"\t{application_cmd} --update <id of existent register>: update an register\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) >= 1:
        money_id = int(args[0])
        moneyRegister = controller.moneyDAO.getFromId(money_id)
        if moneyRegister is None or moneyRegister.id < 0:
            print("It couldn't find a financial register with given id.")
            return
        for i in range(1, len(args)):
            if utils.is_float(args[i]):
                moneyRegister.amount = float(args[i])
            else:
                moneyRegister.description = args[i]
        new_cat = controller.get_category_from(extra_args)
        if new_cat[0]:
            moneyRegister.category = new_cat[1]

        new_account = controller.get_account_from(extra_args)
        if new_account[0]:
            moneyRegister.account = new_account[1]

        new_dt = controller.get_datetime_from(extra_args)
        if new_dt[0]:
            moneyRegister.register_dt = new_dt[1]
        # print('Trying to update register: ' + str(moneyRegister) )
        controller.moneyDAO.update(moneyRegister)

