import os
from dotenv import load_dotenv
import base64
from requests import post
import json

load_dotenv()

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
    # Returns JSON string
    result = post(url, headers=headers, data=data)
    # Convert to Python Dictionary
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

token = get_token()
print(token)
# def get_recommendations():

    