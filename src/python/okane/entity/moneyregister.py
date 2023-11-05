from pyutils.code.props.classproperties import declare_props

from datetime import datetime

class MoneyRegister:
    def __init__(self, args):
        declare_props(
            self,
            props={
                'id': {
                    'prop_type': int,
                    'default_value': -1
                },
                'name': {
                    'prop_type': str,
                    'default_value': ''
                },
                'amount': {
                    'prop_type': float,
                    'default_value': 0.0
                },
                'description': {
                    'prop_type': str,
                    'default_value': ''
                },
                'register_dt': {
                    'default_value': datetime.now()
                },
                'category': {},
                'account': {}
            }
        )
        self.set_properties(args)

    def __str__(self):
        return "(ID: " + str(self.id) + \
                 ', ' + self.description + \
                 ', amount: ' + str(self.amount) + \
                 ', ' + self.category.name + \
                 ', ' + self.account.name + ')'


    def get_register_dt(self):
        return self.register_dt.strftime("%Y-%m-%d")

    def get_data_tuple(self):
        return  (self.description, \
                     self.amount, \
                     self.get_register_dt(),\
                     self.category.id,\
                     self.account.id)
    
    def get_data(self):
        properties_data = self.get_properties()
        properties_data['category'] = properties_data['category'].name
        properties_data['account'] = properties_data['account'].name
        properties_data['register_dt'] = self.get_register_dt()

        return properties_data
