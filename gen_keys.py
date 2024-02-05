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

    try:
        with open(filename, 'r') as file:
            mnemonics = file.readlines()
    except FileNotFoundError:
        mnemonics = []

    # Check if we need to generate a new mnemonic
    if keyId < len(mnemonics):
        mnemonic = mnemonics[keyId].strip()
    else:
        # Generate a new mnemonic if needed
        mnemonic = eth_account.Account.create_mnemonic()
        with open(filename, 'a') as file:
            file.write(mnemonic + '\n')
        mnemonics.append(mnemonic)

    
    acct = eth_account.Account.from_mnemonic(mnemonic=mnemonics[keyId].strip(), account_path=f"m/44'/60'/0'/0/{keyId}")

    msg = eth_account.messages.encode_defunct(challenge)

    sig = acct.sign_message(msg)

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
