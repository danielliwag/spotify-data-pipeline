import logging
import psycopg2
from src.config import get_db_config


def dump_apidata(apidata_tuple):
    db_params = get_db_config()

    query = """
    INSERT INTO stg_spotify_raw (endpoint, payload, user_id)
    VALUES (%s, %s, %s);
    """

    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, apidata_tuple)
        conn.commit()