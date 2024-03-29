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

	#YOUR CODE HERE
    # Initialize Web3 (Dummy provider since we're not interacting with a chain here)
    w3 = Web3()

    private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"
    # Generate a new Ethereum account
    account = eth_account.Account.from_key(private_key)
    eth_addr = account.address

    # Prepare the message for signing
    msg = eth_account.messages.encode_defunct(challenge)

    # Sign the message
    sig = account.sign_message(msg)

    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
# 0xCd0292B199A56CBE019cCA4D9F95D53007b2bCF7 bsc
# 0xCDc40c933e2db76eCd5d72cd9dcFFCEb519B1972 avax