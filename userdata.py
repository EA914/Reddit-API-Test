import requests
import os
from dotenv import load_dotenv
import json  # Import the json module

# Load environment variables from .env file
load_dotenv()

# Get the bearer token from the environment variable
bearer_token = os.getenv('REDDIT_BEARER_TOKEN')

# Set up the headers with the authorization token
headers = {
	'Authorization': f'Bearer {bearer_token}',
	'User-Agent': 'USER AGENT HERE'
}

# Make a GET request to the /api/v1/me endpoint
response = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

# Check if the request was successful
if response.status_code == 200:
	# Format the response JSON with indentation for readability
	formatted_response = json.dumps(response.json(), indent=4)
	print(formatted_response)
else:
	# Print the error message
	print(f'Error: {response.status_code}')
