from okane.entity.recurrentregister import MoneyRecurrentRegister
import datetime


def test_default_values():
    register = MoneyRecurrentRegister({})

    assert register.id == -1
    assert register.amount == 0.0
    assert register.description == ''
    assert isinstance(register.start_dt, datetime.datetime)
    assert register.end_dt is None
    assert register.category is None
    assert register.account is None
    assert register.recurrence == 'monthly'
    assert register.recurrence_number == 1


def test_custom_values():
    custom_start_dt = datetime.datetime(2022, 1, 1)
    custom_end_dt = datetime.datetime(2023, 1, 1)

    args = {
        'id': 1,
        'amount': 100.0,
        'description': 'Test Description',
        'start_dt': custom_start_dt,
        'end_dt': custom_end_dt,
        'category': 'Test Category',
        'account': 'Test Account',
        'recurrence': 'weekly',
        'recurrence_number': 10
    }

    register = MoneyRecurrentRegister(args)

    assert register.id == 1
    assert register.amount == 100.0
    assert register.description == 'Test Description'
    assert register.start_dt == custom_start_dt
    assert register.end_dt == custom_end_dt
    assert register.category == 'Test Category'
    assert register.account == 'Test Account'
    assert register.recurrence == 'weekly'
    assert register.recurrence_number == 10


def test_update_properties():
    register = MoneyRecurrentRegister({})

    new_end_dt = datetime.datetime(2024, 1, 1)

    register.id = 2
    register.amount = 200.0
    register.description = 'Updated Description'
    register.end_dt = new_end_dt
    register.category = 'Updated Category'
    register.account = 'Updated Account'
    register.recurrence = 'daily'
    register.recurrence_number = 5

    assert register.id == 2
    assert register.amount == 200.0
    assert register.description == 'Updated Description'
    assert register.end_dt == new_end_dt
    assert register.category == 'Updated Category'
    assert register.account == 'Updated Account'
    assert register.recurrence == 'daily'
    assert register.recurrence_number == 5
