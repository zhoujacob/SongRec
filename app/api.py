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
    
    songs = [{"name": item["name"], "artist": item["artists"][0]["name"]} for item in json_result]
    return [songs]

# # format should be:
# # http GET 'https://api.spotify.com/v1/recommendations?seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA' \
# #  Authorization:'Bearer 1POdFZRZbvb...qqillRxMr2z' 
# def get_recommendations(token, seed_artists=None, seed_genres=None, seed_tracks=None):
#     url = "https://api.spotify.com/v1/recommendations"

#     headers = get_auth_header(token)
#     params = {
#         'seed_tracks': ','.join(seed_tracks) if seed_tracks else None,
#         'seed_artists': ','.join(seed_artists) if seed_artists else None,
#         'seed_genres': ','.join(seed_genres) if seed_genres else None
#     }

#     response = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=params)
    
#     if response.status_code == 200:
#         json_result = response.json()
#         print(json_result)
#     else:
#         print("Error:", response.status_code)



# # seed_tracks = ["0c6xIDDpzE81m2q797ordA"]  # Example Spotify track ID
# # get_recommendations(token, seed_tracks)
