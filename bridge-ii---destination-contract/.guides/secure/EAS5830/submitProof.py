"""
    We are agnostic about how the students submit their merkle proofs to the on-chain contract
    But if they were to submit using Python, this would be a good way to do it
"""
from web3 import Web3
import json
import os
from eth_account import Account
from web3.middleware import geth_poa_middleware #Necessary for POA chains
import sys
import random
from hexbytes import HexBytes

def hashPair( a,b ):
    """
        The OpenZeppelin Merkle Tree Validator we use sorts the leaves
        https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/MerkleProof.sol#L217
        So you must sort the leaves as well

        Also, hash functions like keccak are very sensitive to input encoding, so the solidity_keccak function is the function to use

        Another potential gotcha, if you have a prime number (as an int) bytes(prime) will *not* give you the byte representation of the integer prime
        Instead, you must call int.from_bytes(prime,'big').

        This function will hash leaves in a Merkle Tree in a way that is compatible with the way the on-chain validator hashes leaves
    """
    if a < b:
        return Web3.solidity_keccak( ['bytes32','bytes32'], [a,b] )
    else:
        return Web3.solidity_keccak( ['bytes32','bytes32'], [b,a] )

def connectTo(chain):
    if chain == 'avax':
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

    if chain == 'bsc':
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

    if chain in ['avax','bsc']:
        w3 = Web3(Web3.HTTPProvider(api_url))
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def generate_primes(n):
        primes = []
        candidate = 2
        while len(primes) < n:
            is_prime = all(candidate % prime != 0 for prime in primes)
            if is_prime:
                primes.append(candidate)
            candidate += 1
        return primes

    

def build_merkle_tree(leaves):
    tree = [Web3.solidity_keccak(['uint256'], [leaf]) for leaf in leaves]  # Convert each prime to its hash
    levels = [tree]
    while len(levels[-1]) > 1:
        level = []
        for i in range(0, len(levels[-1]), 2):
            left = levels[-1][i]
            right = levels[-1][i + 1] if i + 1 < len(levels[-1]) else left
            level.append(Web3.solidity_keccak(['bytes32', 'bytes32'], sorted([left, right])))
        levels.append(level)
    return levels

def get_merkle_proof(tree, index):
    proof = []
    for level in tree[:-1]:
        opposite_index = index ^ 1  # Get the index of the sibling node
        proof.append(level[opposite_index])
        index //= 2  # Move up to the next level
    return proof

if __name__ == "__main__":
    chain = 'avax'

    with open( "contract_info.json", "r" ) as f:
        abi = json.load(f)

    address = "0xb728f421b33399Ae167Ff01Ad6AA8fEFace845F7"

    w3 = connectTo(chain)
    contract = w3.eth.contract( abi=abi, address=address )

    ###
    #YOUR CODE HERE
    ###
    

    primes = generate_primes(8192)
    tree = build_merkle_tree(primes)
    proof = get_merkle_proof(tree, 0)