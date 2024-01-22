import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	# Convert the dictionary to JSON
	json_data = json.dumps(data)

	# Prepare the request to add the data to IPFS
	response = requests.post(f"{IPFS_API_URL}/add", files={"file": json_data})

	# Extract the CID from the response
	cid = json.loads(response.text)["Hash"]
	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	
	# Prepare the request to get data from IPFS using the CID
	response = requests.get(f"{IPFS_API_URL}/cat/{cid}")

	# Extract the content from the response
	content = response.text

	# Parse the content based on the specified content type
	if content_type == "json":
			data = json.loads(content)
			assert isinstance(data, dict), "get_from_ipfs should return a dict"
			return data
	else:
			# You can add more content types handling here if needed
			return content
