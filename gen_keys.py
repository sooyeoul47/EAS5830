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
    mnemonics = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            mnemonics = file.readlines()

    # Check if we need to generate a new mnemonic
    if len(mnemonics) <= keyId:
        new_mnemonic = w3.eth.account.create_with_mnemonic()
        mnemonics.append(new_mnemonic + '\n')  # Add new mnemonic with newline for storage
        with open(filename, 'w') as file:
            file.writelines(mnemonics)

    mnemonic = mnemonics[keyId].strip()
    acct = w3.eth.account.from_mnemonic(mnemonic)
    eth_addr = acct.address


    msg = eth_account.messages.encode_defunct(challenge)
    sig = acct.sign_message(msg)
	#YOUR CODE HERE
    
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
