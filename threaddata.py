import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get the bearer token from the environment variable
bearer_token = os.getenv('REDDIT_BEARER_TOKEN')

# Set up the headers with the authorization token
headers = {
	'Authorization': f'Bearer {bearer_token}',
	'User-Agent': 'USER AGENT HERE'
}

# Function to retrieve post titles
def get_post_titles(after=None):
	params = {
		'limit': 100  # Adjust the limit as needed (max is 100 per request)
	}
	if after:
		params['after'] = after

	# Make a GET request to the user's submitted posts endpoint
	response = requests.get(f'https://oauth.reddit.com/user/supamariolox/submitted', headers=headers, params=params)

	if response.status_code == 200:
		data = response.json()
		posts = data['data']['children']
		for post in posts:
			title = post['data']['title']
			print(f"Title: {title}")
		after = data['data']['after']
		if after:
			get_post_titles(after=after)  # Recursively get more titles if there are more pages
	else:
		print(f'Error: {response.status_code}')

# Retrieve and print post titles
get_post_titles()
