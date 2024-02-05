from web3 import Web3, Account
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

    # Ensure the directory for the filename exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    private_keys = []

    # Try to read existing private keys from the file
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            private_keys = file.read().splitlines()

    # Check if we need to generate a new private key
    if keyId >= len(private_keys):
        # Generate a new account
        new_account = w3.eth.account.create()
        private_key = new_account.privateKey.hex()
        # Append the new private key to the list
        private_keys.append(private_key)
        # Save the new private key list to the file
        with open(filename, 'w') as file:
            file.write("\n".join(private_keys))
    else:
        # Use the existing private key
        private_key = private_keys[keyId]

    # Derive the account address from the private key
    eth_addr = w3.eth.account.privateKeyToAccount(private_key).address

    # Sign the challenge
    sig = w3.eth.account.sign_message(w3.keccak(text=challenge), private_key=private_key)

	#YOUR CODE HERE
    
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
