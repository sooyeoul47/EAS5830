from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time


bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)
api_url = "https://eth-mainnet.g.alchemy.com/v2/3stBMV-y3BpNCMQpK0BQV6kLWEmlfKdF"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
contract = web3.eth.contract(address=contract_address, abi=abi)


def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	data = {'owner': "", 'image': "", 'eyes': "" }
	
	#YOUR CODE HERE	
	# Get the Token URI
	owner = contract.functions.ownerOf(apeID).call()
	token_uri = contract.functions.tokenURI(apeID).call()

	# Fetch metadata from IPFS
	ipfs_gateway = "https://ipfs.io/ipfs/"
	metadata_url = token_uri.replace("ipfs://", ipfs_gateway)
	response = requests.get(metadata_url)
	metadata = response.json()

	# Extract image and eyes from metadata
	image = metadata['image'].replace("ipfs://", ipfs_gateway)
	eyes = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Eyes')

	data = {'owner': owner, 'image': image, 'eyes': eyes}

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

