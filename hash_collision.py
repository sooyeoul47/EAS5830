import hashlib
import os

def hash_collision(k):
    if not isinstance(k,int):
        print( "hash_collision expects an integer" )
        return( b'\x00',b'\x00' )
    if k < 0:
        print( "Specify a positive number of bits" )
        return( b'\x00',b'\x00' )
   
    #Collision finding code goes here
    x = os.urandom(16)
    y = os.urandom(16)

    hex_digits = k // 4
    
    while True:
        x_hash = hashlib.sha256(x).hexdigest()
        y_hash = hashlib.sha256(y).hexdigest()

        # Check if the last k bits (or hex_digits/4 of the hash) match
        if x_hash[-hex_digits:] == y_hash[-hex_digits:]:
            break
        else:
            # Generate new random values for x and y
            x = os.urandom(16)
            y = os.urandom(16)
            while y == x:  # Ensure y is different from x
                y = os.urandom(16)

    return( x, y )




