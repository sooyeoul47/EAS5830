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

    # w3 = Web3()

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            private_keys = file.readlines()
        if keyId < len(private_keys):
            private_key = private_keys[keyId].strip()
        else:
            new_account = eth_account.Account.create()
            private_key = new_account.key.hex()
            with open(filename, 'a') as file:
                file.write(private_key + '\n')
    else:
        new_account = eth_account.Account.create()
        private_key = new_account.key.hex()
        with open(filename, 'w') as file:
            file.write(private_key + '\n')

    account = eth_account.Account.from_key(private_key)

    # If 'challenge' is a bytes object, use it directly
    msg = eth_account.messages.encode_defunct(text=challenge)
    sig = account.sign_message(msg)

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
