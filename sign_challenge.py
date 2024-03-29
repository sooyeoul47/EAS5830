import eth_account
from eth_account import Account
from eth_account.messages import encode_defunct

def sign_challenge(challenge):
    """
        Takes a challenge (string)
        Returns addr, sig
        where addr is an ethereum address (in hex)
        and sig is a signature (in hex)
    """
    private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"
    ####
    #YOUR CODE HERE
    ####
    account = Account.from_key(private_key)
    address = account.address
    
    # Encode the challenge message
    encoded_message = encode_defunct(text=challenge)
    
    # Sign the encoded message
    signed_message = Account.sign_message(encoded_message, private_key)
    
    # Return the address and the signature in hexadecimal format
    return address, signed_message.signature.hex()

if __name__ == "__main__":
    """
        This may help you test the signing functionality of your code
    """
    import random 
    import string

    letters = string.ascii_letters
    challenge = ''.join(random.choice(string.ascii_letters) for i in range(32)) 

    addr, sig = sign_challenge(challenge)

    eth_encoded_msg = eth_account.messages.encode_defunct(text=challenge)

    if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == addr:
        print( f"Success: signed the challenge {challenge} using address {addr}!")
    else:
        print( f"Failure: The signature does not verify!" )
        print( f"signature = {sig}" )
        print( f"address = {addr}" )
        print( f"challenge = {challenge}" )

