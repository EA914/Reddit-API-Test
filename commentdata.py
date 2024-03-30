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

# Function to retrieve comment history
def get_comment_history(after=None):
	params = {
		'limit': 100  # Adjust the limit as needed (max is 100 per request)
	}
	if after:
		params['after'] = after

	# Make a GET request to the user's comments endpoint
	response = requests.get(f'https://oauth.reddit.com/user/supamariolox/comments', headers=headers, params=params)

	if response.status_code == 200:
		data = response.json()
		comments = data['data']['children']
		for comment in comments:
			body = comment['data']['body']
			created_utc = comment['data']['created_utc']
			print(f"Date: {created_utc}, Comment: {body}")
		after = data['data']['after']
		if after:
			get_comment_history(after=after)  # Recursively get more comments if there are more pages
	else:
		print(f'Error: {response.status_code}')

# Retrieve and print comment history
get_comment_history()
