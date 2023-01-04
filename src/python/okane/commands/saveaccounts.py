

def execute(args, extra_args, controller):
    if len(args) == 1:
        controller.accountDAO.saveAccount(args[0])
        print("Account saved!")
    else:
        print("Missing account name")
        print("Usage: python -m okane -sa <new-account-to-be-created>")
