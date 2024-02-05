from web3 import Web3
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



rpc_url = "https://api.avax-test.network/ext/bc/C/rpc" 
contract_address = Web3.to_checksum_address("0x85ac2e065d4526FBeE6a2253389669a12318A412")
wallet_address = "0xDEdA37C517eF097c10D6501A33de377F194660a5"
private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

web3 = Web3(Web3.HTTPProvider(rpc_url))

with open('/home/codio/workspace/NFT.abi', 'r') as f:
	abi = json.load(f) 
     
nft_contract = web3.eth.contract(address=contract_address, abi=abi)


def claim_nft(account, nonce):
    transaction = nft_contract.functions.claim(account.address, nonce).buildTransaction({
        'chainId': 43113,
        'gas': 1000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(account.address),
    })
    signed_txn = account.signTransaction(transaction)
    return web3.eth.sendRawTransaction(signed_txn.rawTransaction)


if __name__ == '__main__':
    """
        Test your function
    """
    account = Account.from_key(private_key)
    nonce = web3.toHex(text='5')
    claim_nft(account, nonce)
    

    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )