import os
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

CACHE_PATH = os.getenv(
    "SPOTIPY_CACHE_PATH",
    str(Path(__file__).resolve().parent / ".cache"),
)


def get_spotify_auth_manager():
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope=os.getenv("SCOPE"),
        cache_path=CACHE_PATH,
        open_browser=False,
    )

    if auth_manager.get_cached_token() is None:
        raise RuntimeError(
            f"Spotify auth cache not found at '{CACHE_PATH}'. "
            "Create the cache file by authorizing locally once, "
            "then mount it into Airflow or set SPOTIPY_CACHE_PATH."
        )

    return auth_manager


def get_access():
    return spotipy.Spotify(auth_manager=get_spotify_auth_manager())


def get_db_config():
    return {
        "host": os.getenv("DB_HOST"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
    }