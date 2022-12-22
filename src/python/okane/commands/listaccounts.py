

def execute(args, extra_args, controller):
    if len(args) == 0:
        account_list = controller.accountDAO.getAll()
        for account in account_list:
            row_data = (account.id, account.name)
            row_text = 'Id: %s\tAccount: %s'
            # row_text = 'Id: %s\tAccount: %s'
            print(row_text % row_data )
