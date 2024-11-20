import unittest
import os
import json
from unittest.mock import patch, MagicMock
from src.main import load_songs, group_songs_into_playlists, check_env_vars

class TestMain(unittest.TestCase):

    def setUp(self):
        """Set up any preconditions for the tests."""
        self.test_json_data = {
                "songs": [
                    {
                        "alltime": False,
                        "artist": "Spiderbait",
                        "country": "Australia",
                        "id": "1",
                        "pollyear": 1996,
                        "position": 1,
                        "releaseyear": "1996",
                        "track": "Buy Me a Pony"
                        },
                    {
                        "alltime": True,
                        "artist": "Tool",
                        "country": "USA",
                        "id": "2",
                        "pollyear": 1998,
                        "position": 2,
                        "releaseyear": "1996",
                        "track": "Stinkfist"
                        }
                    ]
                }
        self.test_json_path = os.path.join(os.path.dirname(__file__), "../data/test_songs.json")
        os.makedirs(os.path.dirname(self.test_json_path), exist_ok=True)
        with open(self.test_json_path, 'w') as file:
            json.dump(self.test_json_data, file)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.test_json_path):
            os.remove(self.test_json_path)

    def test_load_songs(self):
        """Test that the load_songs function correctly loads JSON data."""
        with patch("src.main.os.path.join", return_value=self.test_json_path):
            songs = load_songs()
        self.assertEqual(len(songs), 2)
        self.assertEqual(songs[0]["artist"], "Spiderbait")
        self.assertEqual(songs[1]["artist"], "Tool")
        self.assertEqual(songs[0]["track"], "Buy Me a Pony")
        self.assertEqual(songs[1]["track"], "Stinkfist")
        self.assertEqual(songs[0]["pollyear"], 1996)
        self.assertEqual(songs[1]["pollyear"], 1998)
        self.assertEqual(songs[0]["position"], 1)
        self.assertEqual(songs[1]["position"], 2)
        self.assertEqual(songs[0]["alltime"], False)
        self.assertEqual(songs[1]["alltime"], True)
    
    def test_group_songs_into_playlists(self):
        """Test that songs are grouped correctly into playlists."""
        playlists = group_songs_into_playlists(self.test_json_data["songs"])
        self.assertIn("Triple J Top 100 1996", playlists)
        self.assertIn("Triple J Top 100 1998 All-Time", playlists)
        self.assertEqual(len(playlists["Triple J Top 100 1996"]), 1)
        self.assertEqual(len(playlists["Triple J Top 100 1998 All-Time"]), 1)
        self.assertEqual(playlists["Triple J Top 100 1996"][0]["artist"], "Spiderbait")
        self.assertEqual(playlists["Triple J Top 100 1998 All-Time"][0]["artist"], "Tool")
        self.assertEqual(playlists["Triple J Top 100 1996"][0]["track"], "Buy Me a Pony")
        self.assertEqual(playlists["Triple J Top 100 1998 All-Time"][0]["track"], "Stinkfist")

    def test_check_env_vars_missing(self):
        """Test that the check_env_vars function correctly checks for missing environment variables."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as cm:
                check_env_vars()
            self.assertEqual(cm.exception.code, 1)

    def test_check_env_vars_present(self):
        """Test that the check_env_vars function correctly returns environment variables."""
        with patch.dict(os.environ, {
            "SPOTIFY_CLIENT_ID": "test_id",
            "SPOTIFY_CLIENT_SECRET": "test_secret",
            "SPOTIFY_REDIRECT_URI": "http://test_uri"
            }):
            spotify_client_id, spotify_client_secret, spotify_redirect_uri = check_env_vars()
            self.assertEqual(spotify_client_id, "test_id")
            self.assertEqual(spotify_client_secret, "test_secret")
            self.assertEqual(spotify_redirect_uri, "http://test_uri")

if __name__ == '__main__':
    unittest.main()
