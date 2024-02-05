from web3 import Web3
from web3.contract import Contract
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
web3 = Web3(Web3.HTTPProvider("https://testnet.snowtrace.io/address/0xDEdA37C517eF097c10D6501A33de377F194660a5"))


# with open('/home/codio/workspace/NFT.abi', 'r') as f:
# 	abi = json.load(f) 
     
nft_contract = Web3.eth.contract(address=contract_address, abi='/home/codio/workspace/NFT.abi')

def claim_nft(account):
    nonce = os.urandom(16)  # Generate a random nonce
    # Prepare transaction
    tx = nft_contract.functions.claim(web3.toHex(nonce)).buildTransaction({
        'from': account.address,
        'gas': 1000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(account.address),
    })
    signed_tx = web3.eth.account.sign_transaction(tx, account.key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

if __name__ == '__main__':
    """
        Test your function
    """
    private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"

    account = web3.eth.account.from_key(private_key)

    claim_nft(account)

    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )

