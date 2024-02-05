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
            mnemonics = file.read().splitlines()
    else:
        mnemonics = []

    # Check if we need to generate a new mnemonic
    if keyId >= len(mnemonics):
        # Generate a new account
        new_account = Account.create()
        mnemonic = new_account.address # This is a simplification; normally, we'd use a mnemonic phrase
        # Append the new mnemonic (in this case, using the address as a placeholder)
        mnemonics.append(mnemonic)
        # Save the new mnemonic list
        with open(filename, 'w') as file:
            file.write("\n".join(mnemonics))
    else:
        # Use the existing mnemonic (here, using the address as a mnemonic, which is not standard)
        mnemonic = mnemonics[keyId]
        new_account = Account.from_key(mnemonic)

    # Account details
    private_key = new_account.key
    eth_addr = new_account.address

    # Encode the challenge
    msg = eth_account.messages.encode_defunct(text=challenge)

    # Sign the message
    sig = Account.sign_message(msg, private_key=private_key)

	#YOUR CODE HERE
    
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
