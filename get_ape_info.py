from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time


bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)
api_url = "https://gateway.pinata.cloud/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/1"
provider = HTTPProvider(api_url)
web3 = Web3(provider)
headers = {
        "pinata_api_key": "4d1ca1406d39d453fb23",
        "pinata_secret_api_key": "102a7edffa23ac45f84fd12813211f9de296f9500341e7dfcfc0590d0d3486f5"
}
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
	try:
		data['owner'] = contract.functions.ownerOf(apeID).call()
		token_uri = contract.functions.tokenURI(apeID).call()
	except Exception as e:
		print(f"Error accessing contract: {e}")
		return data

	# Fetch metadata from IPFS
	# Replace the IPFS URL prefix with a public gateway URL
	metadata_url = token_uri.replace('ipfs://', 'https://ipfs.io/ipfs/')
	try:
		response = requests.get(metadata_url, headers=headers)
		metadata = response.json()

		data['image'] = metadata.get('image', "")
		attributes = metadata.get('attributes', [])
		for attr in attributes:
			if attr['trait_type'] == 'Eyes':
				data['eyes'] = attr['value']
				break
	except Exception as e:
		print(f"Error fetching metadata: {e}")
	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

