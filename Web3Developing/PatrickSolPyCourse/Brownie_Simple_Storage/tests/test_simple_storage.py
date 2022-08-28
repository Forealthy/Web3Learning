# test file must start with "test_"
from brownie import SimpleStorage, accounts

def test_starting_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert expected == starting_value

def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    simple_storage.store(15, {"from": account})
    expected = 15
    updated_value = simple_storage.retrieve()
    # Assert
    assert expected == updated_value
