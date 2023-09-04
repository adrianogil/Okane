from okane.utils import utils

def get_cmd_flags():
    return ["-d", "--delete"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -d <id-of-register-to-be-deleted>: delete a register\n"
    help_usage_str += f"\t{application_cmd} --delete <id-of-register-to-be-deleted>: delete a register\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 1 and utils.is_int(args[0]):
        money_id = int(args[0])
        moneyRegister = controller.moneyDAO.getFromId(money_id)
        if moneyRegister is None or moneyRegister.id < 0:
            print("It couldn't find a financial register with given id.")
            return
        controller.moneyDAO.delete(moneyRegister)
        print('Register deleted!')

        # TODO: add dynamic properties to MoneyRegister
        # moneyRegister.print_properties()
    else:
        print("Missing register name")
        print("Usage: python -m okane -d <id-of-register-to-be-deleted>")
