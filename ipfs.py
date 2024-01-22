import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	 # Convert the dictionary to JSON
	json_data = json.dumps(data)

	# Pin the JSON data to IPFS using Pinata
	response = requests.post('https://api.pinata.cloud/pinning/pinJSONToIPFS', json=json_data, headers={'Content-Type': 'application/json'})

	cid = response.json()['IpfsHash']

	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	
	response = requests.get(f'https://gateway.pinata.cloud/ipfs/{cid}')
	data = response.json()
	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
