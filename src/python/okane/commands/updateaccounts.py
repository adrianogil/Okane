

def execute(args, extra_args, controller):
    if len(args) == 2:
        cat_id = int(args[0])
        account = controller.accountDAO.getAccountFromId(cat_id)
        if account is None or account.id < 0:
            print("It couldn't find account with the given id: " + str(cat_id))
        account.name = args[1]
        controller.accountDAO.update(account)
