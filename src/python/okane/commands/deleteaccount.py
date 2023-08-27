from okane.utils import utils

def get_cmd_flags():
    return ["-da", "--delete-account"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -da <new-account-to-be-deleted>: delete an account\n"
    help_usage_str += f"\t{application_cmd} --delete-account <new-account-to-be-deleted>: delete an account\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 1:
        if utils.is_int(args[0]):
            cat_id = int(args[0])
            account = controller.accountDAO.getAccountFromId(cat_id)
        else:
            account_name = args[0]
            account = controller.accountDAO.getAccount(account_name)
        if account is None or account.id < 0:
            print("It couldn't find account with the given parameter: " + args[0])
            return

        controller.accountDAO.delete(account)
        print("Account deleted!")
        account.print_properties()
    else:
        print("Missing account name")
        print("Usage: python -m okane -da <new-account-to-be-deleted>")
