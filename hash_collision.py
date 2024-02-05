import hashlib
import os

def hash_collision(k):
    if not isinstance(k,int):
        print( "hash_collision expects an integer" )
        return( b'\x00',b'\x00' )
    if k < 0:
        print( "Specify a positive number of bits" )
        return( b'\x00',b'\x00' )
   
    while True:
        # Generate two random strings
        x = os.urandom(16)  # You can adjust the length as needed
        y = os.urandom(16)

        # Compute SHA256 hashes
        hash_x = hashlib.sha256(x).hexdigest()
        hash_y = hashlib.sha256(y).hexdigest()

        # Convert hexdigests to binary strings
        bin_x = bin(int(hash_x, 16))[-k:]  # Get the last k bits
        bin_y = bin(int(hash_y, 16))[-k:]  # Get the last k bits

        # Check if the last k bits match
        if bin_x == bin_y:
            return (x, y)




