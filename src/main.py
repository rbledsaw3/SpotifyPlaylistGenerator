import json
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import sys

# Checking environment variables
def check_env_vars():
    missing_vars = []

    # Spotify API credentials
    spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
    spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    spotify_redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

    if not spotify_client_id:
        missing_vars.append('SPOTIFY_CLIENT_ID')
    if not spotify_client_secret:
        missing_vars.append('SPOTIFY_CLIENT_SECRET')
    if not spotify_redirect_uri:
        missing_vars.append('SPOTIFY_REDIRECT_URI')

    if missing_vars:
        print(f"Error: The following environment variables need to be set: {', '.join(missing_vars)}")
        sys.exit(1)

    return spotify_client_id, spotify_client_secret, spotify_redirect_uri

# Load JSON file from ./data/songs.json
def load_songs():
    file_path = os.path.join(os.path.dirname(__file__), '../data/songs.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data["songs"]

# Deal with rate limiting API calls
def execute_with_rate_limit(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status != 429:
                raise e
            retry_after = int(e.headers.get("Retry-After", 1))
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)

# Group songs by year and playlist type
def group_songs_into_playlists(songs):
    playlists = {}
    for song in songs:
        playlist_name = f"Triple J Top 100 {song['pollyear']}{' All-Time' if song['alltime'] else ''}"
        if playlist_name not in playlists:
            playlists[playlist_name] = []
        playlists[playlist_name].append(song)
    return playlists

# Creating playlists and adding songs
def create_playlist(playlist_name, songs):
    # Ensure Top 100 songs are sorted in descending order, i.e. rank 100 song is first, rank 1 is last
    songs_sorted = sorted(songs, key=lambda x: x["position"], reverse=True)

    user_id = execute_with_rate_limit(sp.current_user)["id"]
    playlist = execute_with_rate_limit(
            sp.user_playlist_create,
            user_id,
            playlist_name,
            description=f"Playlist for {playlist_name}"
            )
    playlist_id = playlist["id"]

    uris = []
    for song in songs_sorted:
        query = f"track:{song['track']} artist:{song['artist']}"
        results = execute_with_rate_limit(
                sp.search,
                q=query,
                type="track",
                limit=1
                )
        if results["tracks"]["items"]:
            uris.append(results["tracks"]["items"][0]["uri"])
        else:
            print(f"Song not found: {song['track']} by {song['artist']}")

    #Add songs to playlist in chucks of 100
    for i in range(0, len(uris), 100):
        execute_with_rate_limit(
                sp.playlist_add_items,
                playlist_id,
                uris[i:i+100]
                )
    print(f"Playlist '{playlist_name}' created successfully!")

def main():
    spotify_client_id, spotify_client_secret, spotify_redirect_uri = check_env_vars()

    global sp
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri=spotify_redirect_uri,
        scope='playlist-modify-public playlist-modify-private'
    ))

    songs = load_songs()
    playlists = group_songs_into_playlists(songs)
    for playlist_name, songs in playlists.items():
        create_playlist(playlist_name, songs)

if __name__ == "__main__":
    main()
