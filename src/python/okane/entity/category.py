from pyutils.code.props.classproperties import declare_props


class Category:
    def __init__(self, name, id=-1, parent=None):
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
                'parent': {
                    'default_value': None
                }
            }
        )
        self.id = id
        self.name = name
        self.parent = parent
