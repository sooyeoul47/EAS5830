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
            mnemonics = file.readlines()
        if keyId < len(mnemonics):
            # Use existing mnemonic
            mnemonic = mnemonics[keyId].strip()
        else:
            # Generate a new mnemonic and append it
            mnemonic = eth_account.Account.create().address
            with open(filename, 'a') as file:
                file.write(mnemonic + '\n')
    else:
        # File does not exist, generate a new mnemonic
        mnemonic = eth_account.Account.create().address
        with open(filename, 'w') as file:
            file.write(mnemonic + '\n')

    
    # Create an account from the mnemonic
    account = eth_account.Account.from_key(mnemonic)

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
