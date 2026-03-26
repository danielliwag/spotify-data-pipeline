import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    # Token request
    token_url = 'https://accounts.spotify.com/api/token'
    data = {'grant_type': 'client_credentials'}

    response = requests.post(token_url, auth=(client_id, client_secret), data=data)
    access_token = response.json().get('access_token')
    return access_token