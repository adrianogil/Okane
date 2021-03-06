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

        if 'account' in args:
            self.account = args['account']

    def __str__(self):
        return "(ID: " + str(self.id) + \
                 ', ' + self.description + \
                 ', amount: ' + str(self.amount) + \
                 ', ' + self.category.name + \
                 ', ' + self.account.name + ')'


    def get_register_dt(self):
        return self.register_dt.strftime("%Y-%m-%d %H:%M:%S")

    def get_data_tuple(self):
        return  (self.description, \
                     self.amount, \
                     self.get_register_dt(),\
                     self.category.id,\
                     self.account.id)



