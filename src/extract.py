import requests
import psycopg2
from psycopg2.extras import Json
from src.config import get_access, get_db_config


def extract_apidata(endpoint, latest_dt):
    
    sp = get_access()

    try:
        raw_data = sp.current_user_recently_played(limit=50, after=latest_dt)

        return endpoint, Json(raw_data), 200

    except spotipy.exceptions.SpotifyException as e:
        print(f'Error occurred: {e.http_status} - {e.msg}')
    except Exception as e:
        print(f'An error occured: {e}')
        return None

def get_cursor():
    db_params = get_db_config()
    
    query = """
    SELECT MAX((item->>'played_at')::timestamptz)
    FROM stg_spotify_raw, 
         jsonb_array_elements(payload->'items') AS item;
    """
    
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchone()
                
                if result and result[0]:
                    # result[0] is already a Python datetime object thanks to psycopg2
                    dt_object = result[0]
                    
                    # Spotify needs MILLISECONDS as an integer
                    # Using .timestamp() gives seconds, so we multiply by 1000
                    return int(dt_object.timestamp() * 1000)
                
                return None
    except Exception as e:
        print(f"Error retrieving cursor: {e}")
        return None