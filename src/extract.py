import requests
from psycopg2.extras import Json
from src.config import get_access_token


def extract_apidata(endpoint, after_ms=None):
    try:
        access_token = get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        url = f'https://api.spotify.com/v1/{endpoint}'

        params = {'limit': 50}
        if after_ms:
            params['after'] = after_ms

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        api_data = response.json()

        return endpoint, Json(api_data), response.status_code

    except Exception as e:
        print(f'An error occured: {e}')
        return None


