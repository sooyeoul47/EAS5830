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


bayc_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
contract_address = Web3.to_checksum_address(bayc_address)
web3 = Web3(Web3.HTTPProvider("https://api.avax-test.network/ext/bc/C/rpc"))


with open('/home/codio/workspace/NFT.abi', 'r') as f:
	abi = json.load(f) 
     
nft_contract = web3.eth.contract(address=contract_address, abi=abi)

def claim_nft(private_key):
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.getTransactionCount(account.address)
    tx = nft_contract.functions.claim(os.urandom(16)).buildTransaction({
        'from': account.address,
        'gas': 1000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f"Transaction hash: {tx_hash.hex()}")
    return tx_hash

if __name__ == '__main__':
    """
        Test your function
    """
    private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

    claim_nft(private_key)

    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )

