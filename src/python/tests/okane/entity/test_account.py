import pytest

from okane.entity.account import Account


def test_account_initialization():
    account_name = "Checking Account"
    account = Account(account_name)

    # Test if the account is created with the correct name
    assert account.name == account_name

    # The ID should be set to the default value as per declare_props
    assert account.id == -1


def test_account_id_setter():
    account = Account("Savings Account")

    # Test setting the ID to a new value
    new_id = 100
    account.id = new_id
    assert account.id == new_id

    # Test setting the ID to the default value when set to None
    account.id = None
    assert account.id == -1


def test_account_name_setter():
    account = Account("Initial Account")

    # Set a new name and check if it reflects
    new_name = "Renamed Account"
    account.name = new_name
    assert account.name == new_name

    # Set name to None and check if it defaults to empty string
    account.name = None
    assert account.name == ''
