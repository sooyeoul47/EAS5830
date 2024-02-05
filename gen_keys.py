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

    mnemonics = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            mnemonics = file.readlines()

    mnemonics = [m.strip() for m in mnemonics]

    if keyId >= len(mnemonics):
        # Generate a new mnemonic if needed
        mnemonic = Account.create().address
        mnemonics.append(mnemonic)
        with open(filename, 'a') as file:
            file.write(f"{mnemonic}\n")
    else:
        # Use existing mnemonic
        mnemonic = mnemonics[keyId]

   # Initialize web3 (use the Ethereum test network)
    w3 = Web3()

    # Create account from mnemonic
    account = w3.eth.account.privateKeyToAccount(mnemonic)

    # Prepare the message
    msg = encode_defunct(challenge)

    # Sign the message
    sig = account.sign_message(msg)

    # Verify the signature (as an assertion in your actual code)
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
