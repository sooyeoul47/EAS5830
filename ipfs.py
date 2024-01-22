import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

	headers = {
			"accept": "application/json",
			"content-type": "application/json"
	}

	response = requests.post(url, headers=headers)

	# Extract the CID
	cid = response.json()["IpfsHash"]


	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	
	# Pinata IPFS gateway URL
	url = f'https://gateway.pinata.cloud/ipfs/{cid}'

	# Make the GET request to retrieve the data
	response = requests.get(url)

	# Error handling
	if response.status_code != 200:
			raise Exception('Error retrieving data from IPFS')

	# Parse the response content as JSON
	data = response.json()

	assert isinstance(data, dict), "get_from_ipfs should return a dict"
	
	return data
