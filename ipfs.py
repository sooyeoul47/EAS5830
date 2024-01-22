import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

	headers = {
        "pinata_api_key": "4d1ca1406d39d453fb23",
        "pinata_secret_api_key": "102a7edffa23ac45f84fd12813211f9de296f9500341e7dfcfc0590d0d3486f5",
		"accept": "application/json",
		"content-type": "application/json"
    }

	response = requests.post(url, headers=headers)
	print(response.text)
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
