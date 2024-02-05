from web3 import Web3
import eth_account
import os
from eth_account import Account
from eth_account.messages import encode_defunct

def get_keys(challenge,keyId = 0, filename = "eth_mnemonic.txt"):
    """
    Generate a stable private key
    challenge - byte string
    keyId (integer) - which key to use
    filename - filename to read and store mnemonics

    Each mnemonic is stored on a separate line
    If fewer than (keyId+1) mnemonics have been generated, generate a new one and return that
    """

     # Ensure the Web3 instance is using the local provider
    w3 = Web3()

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            if keyId < len(lines):
                mnemonic = lines[keyId].strip()
                # Generate account from mnemonic (This step needs to be adjusted if you want to use mnemonics)
            else:
                # Generate a new account and append the mnemonic
                account = w3.eth.account.create()
                with open(filename, 'a') as file:
                    file.write(account.privateKey.hex() + '\n')
    else:
        # File doesn't exist, generate a new account
        account = w3.eth.account.create()
        with open(filename, 'w') as file:
            file.write(account.privateKey.hex() + '\n')

    msg = eth_account.messages.encode_defunct(text=challenge)

    sig = account.sign_message(msg)

    eth_addr = eth_account.Account.recover_message(msg, signature=sig.signature)

	#YOUR CODE HERE
    
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
