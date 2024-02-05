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
rpc_url = "https://api.avax-test.network/ext/bc/C/rpc"  
private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0" 
contract_address = Web3.to_checksum_address("0x85ac2e065d4526FBeE6a2253389669a12318A412")
account_address = "0xDEdA37C517eF097c10D6501A33de377F194660a5" 

# Load ABI
with open('/home/codio/workspace/NFT.abi', 'r') as abi_definition:
    contract_abi = json.load(abi_definition)

# Setup web3 connection
web3 = Web3(HTTPProvider(rpc_url))

# Load contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

print(f"Transaction sent, TX Hash: {tx_hash.hex()}")

if __name__ == '__main__':
    """
        Test your function
    """
    nonce = web3.toBytes(text="431")

    # Prepare the claim transaction
    claim_txn = contract.functions.claim(account_address, nonce).buildTransaction({
        'chainId': 43113,  # Chain ID for Avalanche Fuji Testnet
        'gas': 700000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(account_address),
    })

    # Sign the transaction
    signed_txn = web3.eth.account.signTransaction(claim_txn, private_key=private_key)

    # Send the transaction
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Get the transaction receipt (might need to wait for it to be mined)
    txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)


    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )