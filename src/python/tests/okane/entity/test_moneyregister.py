from okane.entity.moneyregister import MoneyRegister

from datetime import datetime


# Mock classes for Category and Account
class MockCategory:
    def __init__(self, name, id=-1):
        self.name = name
        self.id = id

class MockAccount:
    def __init__(self, name, id=-1):
        self.name = name
        self.id = id

# Test cases
def test_default_values():
    register = MoneyRegister({})

    assert register.id == -1
    assert register.amount == 0.0
    assert register.description == ''
    assert isinstance(register.register_dt, datetime)
    assert register.category is None
    assert register.account is None
    assert register.confirmed is True

def test_custom_values():
    custom_register_dt = datetime(2022, 1, 1)
    category = MockCategory('Test Category')
    account = MockAccount('Test Account')

    args = {
        'id': 1,
        'amount': 100.0,
        'description': 'Test Description',
        'register_dt': custom_register_dt,
        'category': category,
        'account': account,
        'confirmed': False
    }

    register = MoneyRegister(args)

    assert register.id == 1
    assert register.amount == 100.0
    assert register.description == 'Test Description'
    assert register.register_dt == custom_register_dt
    assert register.category == category
    assert register.account == account
    assert register.confirmed is False

def test_update_properties():
    register = MoneyRegister({})

    new_register_dt = datetime(2024, 1, 1)
    category = MockCategory('Updated Category')
    account = MockAccount('Updated Account')

    register.id = 2
    register.amount = 200.0
    register.description = 'Updated Description'
    register.register_dt = new_register_dt
    register.category = category
    register.account = account
    register.confirmed = False

    assert register.id == 2
    assert register.amount == 200.0
    assert register.description == 'Updated Description'
    assert register.register_dt == new_register_dt
    assert register.category == category
    assert register.account == account
    assert register.confirmed is False

def test_str_method():
    category = MockCategory('Test Category')
    account = MockAccount('Test Account')
    register = MoneyRegister({'category': category, 'account': account})

    expected_str = f"(ID: -1, , amount: 0.0, {category.name}, {account.name})"
    assert str(register) == expected_str

def test_get_register_dt():
    custom_register_dt = datetime(2022, 1, 1)
    register = MoneyRegister({'register_dt': custom_register_dt})

    assert register.get_register_dt() == '2022-01-01'

def test_get_data_tuple():
    category = MockCategory('Test Category', 1)
    account = MockAccount('Test Account', 2)
    register = MoneyRegister({
        'description': 'Test',
        'amount': 50.0,
        'category': category,
        'account': account,
        'confirmed': True
    })

    expected_tuple = ('Test', 50.0, register.get_register_dt(), 1, 2, True)
    assert register.get_data_tuple() == expected_tuple

def test_get_data():
    category = MockCategory('Test Category')
    account = MockAccount('Test Account')
    register = MoneyRegister({'category': category, 'account': account})

    expected_data = {
        'id': -1,
        'amount': 0.0,
        'description': '',
        'register_dt': register.get_register_dt(),
        'category': category.name,
        'account': account.name,
        'confirmed': True
    }
    assert register.get_data() == expected_data
