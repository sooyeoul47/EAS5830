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
    w3 = Web3(Web3.EthereumTesterProvider())

    # Attempt to load mnemonics from file
    try:
        with open(filename, 'r') as file:
            mnemonics = file.readlines()
    except FileNotFoundError:
        mnemonics = []

    # Check if a mnemonic for the current keyId exists, if not generate a new one
    if keyId >= len(mnemonics):
        # Generate new mnemonic and append to the list
        new_mnemonic = eth_account.Account.create().address
        mnemonics.append(new_mnemonic + '\n')
        with open(filename, 'w') as file:
            file.writelines(mnemonics)

    # Use the mnemonic to generate an account
    mnemonic = mnemonics[keyId].strip()
    acct = eth_account.Account.from_key(mnemonic)

    # Sign the challenge
    msg = encode_defunct(challenge)
    sig = acct.sign_message(msg)

    # Verify the signature (This is more of a sanity check as the assertion below does this)
    eth_addr = acct.address

	#YOUR CODE HERE
    
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
