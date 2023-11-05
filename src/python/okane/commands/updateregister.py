from okane.args import ARGS
from okane.utils import utils

from datetime import datetime


def get_cmd_flags():
    return ["-u", "--update"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -u <id of existent register>: update an register\n"
    help_usage_str += f"\t{application_cmd} --update <id of existent register>: update an register\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 0:
        print("Wrong usage! Check arguments:\n")
        print(get_help_usage_str())
        return
    
    interactive_mode = len(args) == 1

    money_id = int(args[0])
    moneyRegister = controller.moneyDAO.getFromId(money_id)
        
    if moneyRegister is None or moneyRegister.id < 0:
        print("It couldn't find a financial register with given id.")
        return
    
    if interactive_mode:
        print("Edit Register:\n")
        new_description = input(f"Description ({moneyRegister.description}): ").strip()
        if new_description:
            moneyRegister.description = new_description

        new_amount = input(f"Amount ({moneyRegister.amount}): ").strip()
        if new_amount:
            moneyRegister.amount = new_amount

        new_cat_name = input(f"Category ({moneyRegister.category.name}): ").strip()
        if new_cat_name:
            new_cat = controller.get_category_from({ARGS.category: new_cat_name})
            if new_cat[0]:
                moneyRegister.category = new_cat[1]

        new_account_name  = input(f"Account ({moneyRegister.account.name}): ").strip()
        if new_account_name:
            new_account = controller.get_category_from({ARGS.account: new_account_name})
            if new_account[0]:
                moneyRegister.category = new_account[1]

        current_dt_str = moneyRegister.register_dt.strftime("%Y-%m-%d")
        new_dt = input(f"Date ({current_dt_str}): ").strip()
        if new_dt:
            moneyRegister.register_dt = datetime.strptime(new_dt, "%Y-%m-%d")
    else:
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
    controller.moneyDAO.update(moneyRegister)
    print('Register updated: ' + str(moneyRegister) )
