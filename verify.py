from web3 import Web3, HTTPProvider
from eth_account.messages import encode_defunct
from web3 import Account
import random
import os
import json

def signChallenge( challenge ):

    w3 = Web3()

    #This is the only line you need to modify
    sk = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

    acct = w3.eth.account.from_key(sk)

    signed_message = w3.eth.account.sign_message( challenge, private_key = acct._private_key )

    return acct.address, signed_message.signature


def verifySig():
    """
        This is essentially the code that the autograder will use to test signChallenge
        We've added it here for testing 
    """

    challenge_bytes = random.randbytes(32)

    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge( challenge )

    w3 = Web3()

    return w3.eth.account.recover_message( challenge , signature=sig ) == address



# Replace these with your actual details
rpc_url = "https://api.avax-test.network/ext/bc/C/rpc"  # Example Avalanche Fuji Testnet RPC URL
private_key = "YOUR_PRIVATE_KEY_HERE"  # WARNING: Keep your private key secure
contract_address = Web3.toChecksumAddress("0x85ac2e065d4526FBeE6a2253389669a12318A412")
account_address = "YOUR_ACCOUNT_ADDRESS_HERE"  # Your Ethereum address

# Load ABI
with open('/mnt/data/NFT.abi', 'r') as abi_definition:
    contract_abi = json.load(abi_definition)

# Setup web3 connection
web3 = Web3(HTTPProvider(rpc_url))
if web3.isConnected():
    print("Connected to the Avalanche Fuji Testnet")
else:
    print("Failed to connect to the Avalanche Fuji Testnet")
    exit()

# Load contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Generate nonce - this is a simplistic example, consider more complex strategies for real use
nonce = web3.toHex(text='unique_nonce')  # Replace 'unique_nonce' with your strategy

# Prepare the claim transaction
account = Account.from_key(private_key)
nonce_for_tx = web3.eth.getTransactionCount(account.address)
transaction = contract.functions.claim(account_address, nonce).buildTransaction({
    'chainId': 43113,  # Avalanche Fuji Testnet Chain ID
    'gas': 3000000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'nonce': nonce_for_tx,
})

# Sign the transaction
signed_txn = account.sign_transaction(transaction)

# Send the transaction
tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(f"Transaction sent, TX Hash: {tx_hash.hex()}")

if __name__ == '__main__':
    """
        Test your function
    """

    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )