from web3 import Web3
from eth_account.messages import encode_defunct
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


rpc_url = "https://eth-mainnet.g.alchemy.com/v2/3stBMV-y3BpNCMQpK0BQV6kLWEmlfKdF" #Set this to a node that you can connect to (e.g. an Alchemy node)
w3 = Web3(Web3.HTTPProvider(rpc_url))
    
contract_address = Web3.to_checksum_address("0x85ac2e065d4526FBeE6a2253389669a12318A412")

my_address = "0xDEdA37C517eF097c10D6501A33de377F194660a5"
my_private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

with open('/home/codio/workspace/NFT.abi', 'r') as f:
	abi = json.load(f) 
     
nft_contract = w3.eth.contract(address=contract_address, abi=abi)

nonce = w3.eth.getTransactionCount(my_address)
random_nonce = w3.toHex(w3.keccak(text="your random string here"))

# Preparing the transaction
claim_txn = nft_contract.functions.claim(random_nonce).buildTransaction({
    'chainId': 43113,  # Chain ID for Avalanche Fuji Testnet
    'gas': 500000,
    'gasPrice': w3.toWei('50', 'gwei'),
    'nonce': nonce,
})

# Signing the transaction
signed_txn = w3.eth.account.signTransaction(claim_txn, private_key=my_private_key)

# Sending the transaction
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)

# def claim_nft():
#     nonce = w3.eth.getTransactionCount(my_address)
#     tx = nft_contract.functions.claim(os.urandom(16)).buildTransaction({
#         'from': my_address,
#         'gas': 1000000,
#         'gasPrice': w3.toWei('50', 'gwei'),
#         'nonce': nonce,
#     })
# def claim_nft(nonce, private_key):
#     # Prepare the transaction
#     txn = nft_contract.functions.claim(nonce).buildTransaction({
#         'chainId': 43113, # Avalanche Fuji Testnet chain ID
#         'from': account_address,
#         'nonce': w3.eth.getTransactionCount(account_address),
#         # Additional parameters like gas and gasPrice might be needed depending on network conditions
#     })
#     signed_tx = w3.eth.account.sign_transaction(tx, my_private_key)
#     tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     return receipt

if __name__ == '__main__':
    """
        Test your function
    """

    


    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )