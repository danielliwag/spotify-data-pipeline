import requests
import pandas as pd
from src.auth import get_access_token


def extract_album(album_id):
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'https://api.spotify.com/v1/albums/{album_id}'

    response = requests.get(url, headers=headers)
    api_data = response.json()

    data = pd.json_normalize(api_data)

    album_df = pd.DataFrame(data)
    
    return album_df
