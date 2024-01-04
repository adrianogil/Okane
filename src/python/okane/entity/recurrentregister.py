from pyutils.code.props.classproperties import declare_props

from datetime import datetime

class MoneyRecurrentRegister:
    def __init__(self, args):


        declare_props(
            self,
            props={
                'id': {
                    'prop_type': int,
                    'default_value': -1
                },
                'amount': {
                    'prop_type': float,
                    'default_value': 0.0
                },
                'description': {
                    'prop_type': str,
                    'default_value': ''
                },
                'start_dt': {
                    'default_value': datetime.now()
                },
                'end_dt': {
                    'default_value': None
                },
                'category': {
                    'default_value': None
                },
                'account': {
                    'default_value': None
                },
                # recurrence_mode: daily, weekly, biweekly, monthly, yearly
                'recurrence': {
                    'prop_type': str,
                    'default_value': 'monthly'
                },
                # recurrence_number <= 0 -> infinite
                'recurrence_number': {
                    'prop_type': int,
                    'default_value': 1
                }
            }
        )
        self.set_properties(args)
