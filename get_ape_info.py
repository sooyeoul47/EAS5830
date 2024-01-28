from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time


#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = "https://gateway.pinata.cloud/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/1"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.toChecksumAddress(bayc_address)
contract = web3.eth.contract(address=contract_address, abi=abi)

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	# Fetch the owner of the ape
	owner = contract.functions.ownerOf(apeID).call()

    # Fetch the token URI (metadata URI)
	token_uri = contract.functions.tokenURI(apeID).call()

    # Convert IPFS URI to HTTP URI
	ipfs_hash = token_uri.split('//')[1]
	metadata_url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"

	response = requests.get(metadata_url)
	metadata = response.json()
	
	image = metadata.get('image', '')
	attributes = metadata.get('attributes', [])
	eyes = next((attr['value'] for attr in attributes if attr['trait_type'] == 'eyes'), '')

	data = {'owner': owner, 'image': image, 'eyes': eyes}
	
	#YOUR CODE HERE	

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

