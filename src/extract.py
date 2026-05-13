import spotipy
import psycopg2
from psycopg2.extras import Json
from src.config import get_access, get_db_config


def get_user():
    sp = get_access()

    try:
        user = sp.me()
        user_id = user['id']
        return user_id
    
    except Exception as e:
        print(f'Error occurred: {e}')


def extract_apidata(endpoint, latest_dt):
    
    sp = get_access()

    try:
        raw_data = sp.current_user_recently_played(limit=50, after=latest_dt)
        user_id = get_user()

        return endpoint, Json(raw_data), user_id

    except spotipy.exceptions.SpotifyException as e:
        print(f'Error occurred: {e.http_status} - {e.msg}')
        return None
    
    except Exception as e:
        print(f'An error occured: {e}')
        return None

def get_cursor():
    db_params = get_db_config()
    
    query = """
    SELECT payload->'cursors'->>'after'
    FROM stg_spotify_raw
    WHERE payload->'cursors'->>'after' IS NOT NULL
    ORDER BY extracted_at DESC
    LIMIT 1;
    """
    
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchone()
                
                if result and result[0]:
                    return result[0] 
                
                return None
    except Exception as e:
        print(f"Error retrieving cursor: {e}")
        return None