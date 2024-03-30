from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import requests
import os
from dotenv import load_dotenv, set_key
import threading

# Load environment variables
load_dotenv()

# Reddit app credentials
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_SECRET')
redirect_uri = 'NGROKURL'	# Update this to your ngrok URL
scopes = 'read submit edit history identity'

# Authorization URL
auth_url = f'https://www.reddit.com/api/v1/authorize?client_id={client_id}&response_type=code&state=random_string&redirect_uri={redirect_uri}&duration=temporary&scope={scopes}'

# Start a simple HTTP server to listen for the redirect
class RedirectHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		global auth_code
		# Extract the authorization code from the URL
		auth_code = self.path.split('code=')[1].split('&')[0]
		# Send a response to the browser
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b'Authorization code received. You can close this window.')
		# Shutdown the HTTP server
		threading.Thread(target=httpd.shutdown).start()

# The port number should match the one specified in your ngrok URL
httpd = HTTPServer(('localhost', 8000), RedirectHandler)

# Open the authorization URL in the default browser
webbrowser.open(auth_url)

# Start the HTTP server to listen for the redirect
httpd.serve_forever()

# Exchange the authorization code for a bearer token
token_url = 'https://www.reddit.com/api/v1/access_token'
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
data = {
	'grant_type': 'authorization_code',
	'code': auth_code,
	'redirect_uri': redirect_uri
}
response = requests.post(token_url, auth=auth, data=data)
bearer_token = response.json()['access_token']

# Update the .env file with the new bearer token
set_key('.env', 'REDDIT_BEARER_TOKEN', bearer_token)
