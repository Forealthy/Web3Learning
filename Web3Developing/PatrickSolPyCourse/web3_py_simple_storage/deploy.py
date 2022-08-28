import json
from eth_typing import Address
from solcx import compile_standard, install_solc
# import solcx [1]
from web3 import Web3 # Web3 is a class
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol","r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# print("installing...")
install_solc("0.6.0")

# compile_sol is a dict
compiled_sol = compile_standard( #if: [1], then: solcx.compile_stamdard()
    {
        "language": "Solidity", # Solidity not solidity
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*":{
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version = "0.6.0",
)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol, file) # dump(A => B)

# get bytecode: stand for the contract itself
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# getting connected to ganache
# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545")) # w3: chain; this is virtual chain, operating one node on ganache
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/ed65331e3c0b498aa871f5dcb6081c47")) # connect to Rinkeby testnet
chain_id = w3.eth.chain_id # chainlist.org to get the chainId
print("chain_id: ",chain_id)
my_address = "0x859B2944F0D81F6a1339a60B25A7508aC40763FF" # my wallet address
private_key = os.getenv("PRIVATE_KEY") # my wallet private key


# create the contract in python
# ABI, bytecode
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# submit the transaction that deploy the contract
# Build the transaction
transaction = SimpleStorage.constructor().buildTransaction(
    # transaction is a dict
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)
# signed_txn = (somethingcode, hash = (), r = (), s = (), v = ())

# Send the transaction
# print("Deploying the contract!")
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction) # method: send_raw_transaction returns hash value

# waiting for the txn to be mined, and get the txn receipt
# print("waiting for the txn to be finished...")
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
'''
print("txn_receipt:",txn_receipt)
print(f"Done! Contract deployed to {txn_receipt.contractAddress}")
'''

# working with this contract
# Address, ABI
# call(), transact
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi = abi)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}") # must call(), otherwise it stand for a function
'''
print(simple_storage.functions.store(15).call()) # function must have returns so we can call() it validly, no returns, it output []
print(f"Now Stored Value {simple_storage.functions.retrieve().call()}")

ouput:
Initial Stored Value 0
15
Now Stored Value 0
'''

# send a real transaction to store the number: 15 !
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce+1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(greeting_transaction, private_key = private_key)
txn_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("updating stored value ...")
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_greeting_hash)
print(simple_storage.functions.retrieve().call())
