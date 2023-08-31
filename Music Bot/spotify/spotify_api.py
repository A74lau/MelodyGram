import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


# spotify api search api: 
    # check for more information: "https://developer.spotify.com/console/get-search-item/""

def search_for_song(token, song_name, index):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token) 
    query = f"?q={song_name}&type=track&limit=20"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = result.json()

    track_id = json_result['tracks']['items'][index]['id']
    track_name = json_result['tracks']['items'][index]['name']
    artists = json_result['tracks']['items'][index]['artists']
    artist_names = ', '.join(
        [artist['name'] for artist in artists]
    )
    link = json_result['tracks']['items'][index]['external_urls']['spotify']

    current_track_info = {
        "id": track_id,
        "name": track_name,
        "artists": artist_names,
        "link": link
    }

    return current_track_info
    



