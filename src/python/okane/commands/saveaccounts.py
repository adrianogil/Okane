
def get_cmd_flags():
    return ["-sa", "--save-account"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -sa <new-account-to-be-created>: save an account\n"
    help_usage_str += f"\t{application_cmd} --save-account <new-account-to-be-created>: save an account\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 1:
        controller.accountDAO.saveAccount(args[0])
        print("Account saved!")
    else:
        print("Missing account name")
        print("Usage: python -m okane -sa <new-account-to-be-created>")
