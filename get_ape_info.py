from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time



#Connect to an Ethereum node
api_url = "https://gateway.pinata.cloud/ipfs/"
provider = HTTPProvider(api_url)
web3 = Web3(provider)


bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = web3.utils.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 
contract = web3.eth.contract(address=contract_address, abi=abi)
############################



def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	# Fetch the owner of the ape
	owner = contract.functions.ownerOf(apeID).call()

	tokenURI = contract.functions.tokenURI(apeID).call()
	metadata_url = tokenURI.replace('ipfs://', 'https://gateway.pinata.cloud/ipfs/')

	metadata_response = requests.get(metadata_url)
	metadata = metadata_response.json()
	
	image = metadata.get('image', '').replace('ipfs://', 'https://gateway.pinata.cloud/ipfs/')
	attributes = metadata.get('attributes', [])
	eyes = next((item['value'] for item in attributes if item['trait_type'] == 'eyes'), None)

	data = {'owner': owner, 'image': image, 'eyes': eyes}
	
	#YOUR CODE HERE	

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

