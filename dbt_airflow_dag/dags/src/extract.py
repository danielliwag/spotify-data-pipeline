import psycopg2
from psycopg2.extras import Json
from config import get_access, get_db_config


def get_user():
    sp = get_access()

    try:
        user_info = sp.me()
        
        return user_info
    
    except Exception as e:
        print(f'Error occurred: {e}')


def extract_apidata(endpoint, cursor):
    
    sp = get_access()

    try:
        raw_data = sp.current_user_recently_played(limit=50, after=cursor)
        user_info = get_user()

        if not raw_data or not raw_data.get('items'):
            print("No new data to extract since last execution.")
            return None
        
        if not user_info:
            print("Failed to retrieve user information.")
            return {}

        return Json(raw_data), Json(user_info), endpoint
    
    except Exception as e:
        print(f'An error occured: {e}')
        raise


def get_cursor():
    db_params = get_db_config()
    
    query = """
    SELECT payload->'cursors'->>'after'
    FROM daniel.stg_spotify_raw
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
        raise