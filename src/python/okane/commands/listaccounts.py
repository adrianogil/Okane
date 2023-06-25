
def get_cmd_flags():
    return ["-la", "--list-accounts"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -la: list all accounts\n"
    help_usage_str += f"\t{application_cmd} --list-accounts: list all accounts\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 0:
        account_list = controller.accountDAO.getAll()
        for account in account_list:
            row_data = (account.id, account.name)
            row_text = 'Id: %s\tAccount: %s'
            # row_text = 'Id: %s\tAccount: %s'
            print(row_text % row_data)
