import datetime

class MoneyRegister:
    def __init__(self, args):
        self.id = -1
        if 'amount' in args:
            self.amount = args['amount']
        else:
            self.amount = 0

        if 'description' in args:
            self.description = args['description']
        else:
            self.description = ""

        if 'register_dt' in args:
            self.register_dt = args['register_dt']
        else:
            self.register_dt = datetime.datetime.now()

        if 'category' in args:
            self.category = args['category']

    def get_register_dt(self):
        return self.register_dt.strftime("%Y-%m-%d %H:%M:%S")


