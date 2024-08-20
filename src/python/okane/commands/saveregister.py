# Command to save a MoneyRegister

from okane.args import ARGS
from okane.utils import utils

from pyutils.cli.flags import verify_flag, get_flag

def get_cmd_flags():
    return ["-s", "--save"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -s <description> <amount> -dt <date> -cs <category> -ac <account>: save a register\n"
    help_usage_str += f"\t{application_cmd} --save <description> <amount> -dt <date> -cs <category> -ac <account>: save a register\n"
    return help_usage_str


def execute(args, extra_args, controller):
    moneyArgs = {}

    recurrent_mode = verify_flag(["-r", "--recurrent"])

    if len(args) >= 2:
        moneyArgs = controller.get_register_data_from(extra_args)
        for i in range(0, 2):
            if utils.is_float(args[i]):
                moneyArgs['amount'] = float(args[i])
            else:
                moneyArgs['description'] = args[i]
        # TODO: Review this part
        # if len(args) > 2:
        #     for i in range(2, len(args)):
        #         if utils.is_float(args[i]):
        #             moneyArgs['amount'] = float(args[i])
        #             moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
        #             controller.moneyDAO.save(moneyRegister)
    else:
        # print("Missing arguments")
        # print("Usage: python3 -m okane -s <description> <amount> -dt <date> -cs <category> -ac <account>")
        from prompt_toolkit import PromptSession
        import fzf_wrapper

        prompt_session = PromptSession()

        moneyArgs = {}
        process_args = {}

        description = prompt_session.prompt("Description: ")

        amount = prompt_session.prompt("Amount: ")
        amount = float(amount)

        datetime_str = prompt_session.prompt("Date: ")
        moneyArgs["register_dt"] = controller.get_datetime_from(datetime_str)

        moneyArgs["category"] = prompt_session.prompt("Category: ")
        if not moneyArgs["category"]:
            categories = controller.categoryDAO.getAll()
            all_categories_names = [category.name for category in categories]
            moneyArgs["category"] = fzf_wrapper.prompt(all_categories_names)[0]

        moneyArgs["account"] = prompt_session.prompt("Account: ")
        if not moneyArgs["account"]:
            accounts = controller.accountDAO.getAll()
            all_accounts_names = [account.name for account in accounts]
            moneyArgs["account"] = fzf_wrapper.prompt(all_accounts_names)[0]

        moneyArgs['description'] = description
        moneyArgs['amount'] = amount

    moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
    if recurrent_mode:
        from okane.entity.recurrentregister import MoneyRecurrentRegister
        moneyRecurrentRegister = MoneyRecurrentRegister(moneyArgs, moneyRegister)
        moneyRecurrentRegister.recurrence = get_flag(["-r", "--recurrent"], default_value="monthly")
        controller.recurrentMoneyDAO.save(moneyRecurrentRegister)
    else:
        moneyRegister.id = controller.moneyDAO.save(moneyRegister)
    print("Registed saved!")
    print(moneyRegister)
