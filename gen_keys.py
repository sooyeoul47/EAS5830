from web3 import Web3
import eth_account
import os

def get_keys(challenge,keyId = 0, filename = "eth_mnemonic.txt"):
    """
    Generate a stable private key
    challenge - byte string
    keyId (integer) - which key to use
    filename - filename to read and store mnemonics

    Each mnemonic is stored on a separate line
    If fewer than (keyId+1) mnemonics have been generated, generate a new one and return that
    """

    w3 = Web3()

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            private_keys = file.readlines()
        # Ensure we have a private key for the given keyId
        if keyId < len(private_keys):
            # Use an existing private key
            private_key = private_keys[keyId].strip()
        else:
            # Generate a new private key and save it
            new_account = eth_account.Account.create()
            private_key = new_account.privateKey.hex()
            with open(filename, 'a') as file:
                file.write(private_key + '\n')
    else:
        # File does not exist, generate a new private key
        new_account = eth_account.Account.create()
        private_key = new_account.privateKey.hex()
        with open(filename, 'w') as file:
            file.write(private_key + '\n')

    
    # Create an account from the mnemonic
    account = eth_account.Account.from_key(private_key)

    # Sign the challenge
    msg = eth_account.messages.encode_defunct(text=challenge)
    sig = account.sign_message(msg)

    # Verify the signature (optional here, as the assertion is already part of the provided code)
    eth_addr = account.address
	#YOUR CODE HERE
    
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
