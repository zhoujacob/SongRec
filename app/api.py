import os
from dotenv import load_dotenv
import base64
from requests import post, get
import json
from urllib.parse import urlencode

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

def get_recommendations(token, seed_artists=None, seed_genres=None, seed_tracks=None):
    url = "https://api.spotify.com/v1/recommendations"

    headers = get_auth_header(token)
    payload = {}
    if seed_artists:
        payload["seed_artists"] = ",".join(seed_artists)
    if seed_genres:
        payload["seed_genres"] = ",".join(seed_genres)
    if seed_tracks:
        payload["seed_tracks"] = ",".join(seed_tracks)
    
    query_result = url + "?" + urlencode(payload)

    result = get(query_result, headers=headers)

    if result.status_code == 200:
        json_result = result.json()
        print(json_result)
    else:
        print(f"Error: {result.status_code}, {result.text}")

token = get_token()
get_recommendations(token, seed_tracks=["<track_id_1>", "<track_id_2>"])
print(token)
