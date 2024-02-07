import os
import base64
import json
import requests

from dotenv import load_dotenv
from requests import post, get

load_dotenv()

# Retrieve Access token Spotify API
def get_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    auth_string = client_id + ":" + client_secret 
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def get_song(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={song_name}&type=track&limit=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    
    if len(json_result) == 0:
        print("No songs with this name exist...")
        return None

    songs = [{"id": item["id"], "name": item["name"], "artist": item["artists"][0]["name"]} for item in json_result]
    return songs  # Return the list directly, not wrapped in another list

def get_recommendations(token, seed_artist, seed_track):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    query = f"?seed_artists={seed_artist}&seed_tracks={seed_track}"

    query_url = url + query 
    result = get(query_url, headers=headers)
    
    json_result = json.loads(result.content)["tracks"]["items"]
    
    if len(json_result) == 0:
        print("No songs with this name exist...")
        return None
    
    return json_result
