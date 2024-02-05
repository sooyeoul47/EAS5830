# from web3 import Web3
# from eth_account.messages import encode_defunct
# import random
# import os
# import json

# def signChallenge( challenge ):

#     w3 = Web3()

#     #This is the only line you need to modify
#     sk = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

#     acct = w3.eth.account.from_key(sk)

#     signed_message = w3.eth.account.sign_message( challenge, private_key = acct._private_key )

#     return acct.address, signed_message.signature


# def verifySig():
#     """
#         This is essentially the code that the autograder will use to test signChallenge
#         We've added it here for testing 
#     """

#     challenge_bytes = random.randbytes(32)

#     challenge = encode_defunct(challenge_bytes)
#     address, sig = signChallenge( challenge )

#     w3 = Web3()

#     return w3.eth.account.recover_message( challenge , signature=sig ) == address


# contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
# web3 = Web3(Web3.HTTPProvider("https://api.avax-test.network/ext/bc/C/rpc"))

# my_address = "0xDEdA37C517eF097c10D6501A33de377F194660a5"
# my_private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

# with open('/home/codio/workspace/NFT.abi', 'r') as f:
# 	abi = json.load(f) 
     
# nft_contract = web3.eth.contract(address=contract_address, abi=abi)

# def claim_nft():
#     nonce = web3.eth.getTransactionCount(my_address)
#     tx = nft_contract.functions.claim(os.urandom(16)).buildTransaction({
#         'from': my_address,
#         'gas': 1000000,
#         'gasPrice': web3.toWei('50', 'gwei'),
#         'nonce': nonce,
#     })
#     signed_tx = web3.eth.account.sign_transaction(tx, my_private_key)
#     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
#     print(f"Transaction hash: {tx_hash.hex()}")
#     return tx_hash

# if __name__ == '__main__':
#     """
#         Test your function
#     """

#     claim_nft()

#     if verifySig():
#         print( f"You passed the challenge!" )
#     else:
#         print( f"You failed the challenge!" )

from web3 import Web3
from eth_account.messages import encode_defunct
import random
import os
import json

def signChallenge(challenge):
    w3 = Web3(Web3.HTTPProvider("https://api.avax-test.network/ext/bc/C/rpc"))

    # Replace "PLACE_HOLDER" with your actual private key used for claiming the NFT
    sk = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

    acct = w3.eth.account.from_key(sk)
    signed_message = acct.sign_message(challenge)

    return acct.address, signed_message.signature

def verifySig():
    challenge_bytes = random.randbytes(32)
    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge(challenge)

    w3 = Web3(Web3.HTTPProvider("https://api.avax-test.network/ext/bc/C/rpc"))

    return w3.eth.account.recover_message(challenge, signature=sig) == address

web3 = Web3(Web3.HTTPProvider("https://api.avax-test.network/ext/bc/C/rpc"))

# Replace these placeholders with your address and private key
my_address = "0xDEdA37C517eF097c10D6501A33de377F194660a5"
my_private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

# Load the ABI file correctly. Ensure the path and file name match your ABI file's location
with open('NFT.abi', 'r') as f:
    abi = json.load(f)

contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
nft_contract = web3.eth.contract(address=contract_address, abi=abi)

def claim_nft():
    nonce = web3.eth.getTransactionCount(my_address)
    tx = nft_contract.functions.claim(os.urandom(16)).buildTransaction({
        'from': my_address,
        'gas': 1000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.sign_transaction(tx, my_private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f"Transaction hash: {tx_hash.hex()}")
    return tx_hash

if __name__ == '__main__':
    claim_nft()

    if verifySig():
        print("You passed the challenge!")
    else:
        print("You failed the challenge!")