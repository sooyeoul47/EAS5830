import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

	headers = {
        "pinata_api_key": "588669fdc80fc9ba4b68",
        "pinata_secret_api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJmYmNkZDQwMi05ZjI3LTRjOTYtYjE4NC0zOGNkNDVmOTkzMDMiLCJlbWFpbCI6InNvb3lvdWxAc2Vhcy51cGVubi5lZHUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6IkZSQTEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX0seyJpZCI6Ik5ZQzEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiNTg4NjY5ZmRjODBmYzliYTRiNjgiLCJzY29wZWRLZXlTZWNyZXQiOiI1ZTgzMmU4MGI3MmFlODc4YzQ0NTY1Zjc2ZmVmMWQxNjQzM2M0MWQwMTlhZDFkZDRkZGQ5Y2EyNjY5ZjQ5ZDJjIiwiaWF0IjoxNzA1OTA1MjQ3fQ.TDGX-LrFWCzB5iTpd0txPaR-Bx3jfl2e8w1i3v9dESw"
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
