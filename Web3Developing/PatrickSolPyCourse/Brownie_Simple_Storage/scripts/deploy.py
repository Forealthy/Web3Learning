from brownie import accounts, config, SimpleStorage, network
# import os
'''
brownie will get all information from "brownie-config.yaml"

'''

def deploy_simple_storage():

    # account = accounts[0] # this only works on ganache, other testnet brownie won't create those account automatically
    
    '''
    after writing :
    brownie accounts new testaccounts1
    and then followed its orders to create an account, then we can write these code:
    account = accounts.load("testaccounts1")
    print(account)
    '''
    
    '''
    after writing my privkey into .env file, we could write these code below:
    account = accounts.add(os.getenv("PRIVATE_KEY")) # Strange! the same privkey product different account???
    print(account)
    '''
    
    # print("accounts_type: {}\naccount_type: {}".format(type(accounts),type(accounts.add(config["wallets"]["from_key"]))))
    account = get_account() # it fetched messages from "brownie-config.yaml" file
    simple_storage = SimpleStorage.deploy({"from": account})
    # as long as we send a transaction, we need {"from": account}, brownie help us set up a chain, and we don't need to write "to"
    # simple_storage is an example, an object, method is to object
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account}) # transaction: <class 'brownie.network.transaction.TransactionReceipt'>
    transaction.wait(1) # wait for one block to confirm the transaction
    # print("transaction_type: {}\ntransaction: {}".format(type(transaction),transaction))
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)

def get_account():
    # print("network.show_active(): ".format(network.show_active()))
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"]) # this returns an account, using ".env" file privkey to create an account

def main():
    deploy_simple_storage()



# run results:
# PS D:\Users\zyk\我的资源\Block Chain Study\web3 developing code\Brownie_Simple_Storage> brownie run scripts/deploy.py --network rinkeby
# INFO: Could not find files for the given pattern(s).
# Brownie v1.19.0 - Python development framework for Ethereum

# BrownieSimpleStorageProject is the active project.

# Running 'scripts\deploy.py::main'...
# accounts_type: <class 'brownie.network.account.Accounts'>
# account_type: <class 'brownie.network.account.LocalAccount'>
# Transaction sent: 0x43d7ad5e9249f1a664bc2be313b70011a4fa0295a57140a270c1c3804be70f69
#   Gas price: 1.000001047 gwei   Gas limit: 369749   Nonce: 15
#   SimpleStorage.constructor confirmed   Block: 11131585   Gas used: 336136 (90.91%)
#   SimpleStorage deployed at: 0xfa61083a51b2a04fB99E413C002EF871955AdE96

# 0
# Transaction sent: 0x098beb79d03d620fbbee8daffacc5b8629c215dbc2d98703475b68409861a6c1
#   Gas price: 1.000001051 gwei   Gas limit: 47905   Nonce: 16
#   SimpleStorage.store confirmed   Block: 11131586   Gas used: 43550 (90.91%)

#   SimpleStorage.store confirmed   Block: 11131586   Gas used: 43550 (90.91%)

# transaction_type: <class 'brownie.network.transaction.TransactionReceipt'>
# transaction: <Transaction '0x098beb79d03d620fbbee8daffacc5b8629c215dbc2d98703475b68409861a6c1'>
# 15

# Ok, something goes wrong, we should use # to comment, but not '''
