from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():

    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account}) 
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()

# export PRIVATE_KEY = 0x9baee9d1a2ed4541c96ed1898fda209d0c5c2980e64fb5dc4b9962068ee0a3cc
# export WEB3_INFURA_PROJECT_ID = ed65331e3c0b498aa871f5dcb6081c47