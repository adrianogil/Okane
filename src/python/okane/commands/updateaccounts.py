
def get_cmd_flags():
    return ["-ua", "--update-account"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -ua <id of existent account>: update an account\n"
    help_usage_str += f"\t{application_cmd} --update-account <id of existent account>: update an account\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 2:
        cat_id = int(args[0])
        account = controller.accountDAO.getAccountFromId(cat_id)
        if account is None or account.id < 0:
            print("It couldn't find account with the given id: " + str(cat_id))
        account.name = args[1]
        controller.accountDAO.update(account)
