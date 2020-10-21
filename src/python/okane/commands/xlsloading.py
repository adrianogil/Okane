import pandas as pd

def execute(args, extra_args, controller):
    if len(args) == 1:
        xls_path = args[0]
        if os.path.isfile(xls_path):
            df = pd.read_excel(xls_path)

            total_registers = len(df)

            keys = df.keys()

            # import pdb; pdb.set_trace() # Start debugger

            for i in range(0, total_registers):
                moneyArgs = {
                    'register_dt' : controller.get_datetime_from({ARGS.datetime:[df[keys[0]][i]]})[1],
                    'category'    : controller.get_category_from({ARGS.category:[df[keys[3]][i].strip()]})[1],
                    'account'     : controller.get_account_from({ARGS.category:[df[keys[4]][i].strip()]})[1],
                    'amount'      : float(df[keys[2]][i]),
                    'description' : df[keys[1]][i].strip()
                }
                moneyRegister = controller.entityFactory.createMoneyRegister(moneyArgs)
                controller.moneyDAO.save(moneyRegister)
                # print(k)
                # print(df[k][0].decode('utf-8', 'ignore'))