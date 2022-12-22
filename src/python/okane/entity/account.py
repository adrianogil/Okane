from pyutils.code.props.classproperties import declare_props


class Account:
    def __init__(self, name):
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
                }
            }
        )
        self.name = name
