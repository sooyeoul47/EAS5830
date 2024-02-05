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
            mnemonics = file.read().splitlines()
    else:
        mnemonics = []


    if len(mnemonics) <= keyId:
        new_account = eth_account.Account.create()
        mnemonic = new_account.privateKey.hex()  # This should be a mnemonic in real use; simplified here for demonstration
        with open(filename, 'a') as file:
            file.write(mnemonic + '\n')
        private_key = mnemonic
    else:
        private_key = mnemonics[keyId]


    # Create account from mnemonic
    account = eth_account.Account.from_key(private_key)
    eth_addr = account.address

    msg = eth_account.messages.encode_defunct(text=challenge)
    sig = account.sign_message(msg)

	#YOUR CODE HERE
    
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
