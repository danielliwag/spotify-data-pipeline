import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

def get_access():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id= os.getenv('CLIENT_ID'),
        client_secret= os.getenv('CLIENT_SECRET'),
        redirect_uri= os.getenv('REDIRECT_URI'),
        scope= os.getenv('SCOPE')
    ))

def get_db_config():
      return {
        "host": os.getenv("DB_HOST"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS")
    }