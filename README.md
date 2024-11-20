# Spotify Playlist Creator

A Python application that uses the Spotify Web API to create playlists from a JSON file of songs. The application dynamically groups songs into playlists by year and type (e.g., all-time playlists) and handles rate-limiting by the Spotify API.  

## Features
- Automatically creates playlists in your Spotify account.
- Groups songs into playlists based on their year and type (e.g., all-time or yearly playlists).
- Handles rate-limiting issues from the Spotify API.
- Logs missing songs if they are not found on Spotify.

---

## Requirements
- Python 3.7 or later.
- Spotify Developer Account.
- Spotipy Python library for interacting with the Spotify Web API.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/rbledsaw3/SpotifyPlaylistGenerator.git
cd SpotifyPlaylistGenerator
```

### 2. Set Up Environment Variables
Set the following environment variables:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI`

You can export them in your terminal for testing:
```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
export SPOTIFY_REDIRECT_URI="http://localhost:8080/callback"
```

Or add them to a `.env` file and use a library like `python-dotenv` to load them.

### 3. Install Dependencies
Create a virtual environment and install dependencies:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 4. Prepare Your JSON File
Place your JSON file in the `data/` folder. The file should be named `songs.json` and follow this format:
```json
{
  "songs": [
    {
      "alltime": false,
      "artist": "Spiderbait",
      "country": "Australia",
      "id": "1",
      "pollyear": 1996,
      "position": 1,
      "releaseyear": "1996",
      "track": "Buy Me a Pony"
    },
    {
      "alltime": false,
      "artist": "Tool",
      "country": "USA",
      "id": "2",
      "pollyear": 1996,
      "position": 2,
      "releaseyear": "1996",
      "track": "Stinkfist"
    }
  ]
}
```

Note: Not all the JSON fields here are used. This is an example of the raw data I started with.

---

## Usage

### Running the Script
Navigate to the `src/` directory and run the script:
```bash
cd src
python main.py
```

The script will:
1. Read the `songs.json` file.
2. Group the songs into playlists. 
3. Create playlists in your Spotify account.
4. Add tracks to the playlists in the correct order.

Note: Playlists are named as follows "Triple J Top 100 {year}{ alltime if alltime is true}"). Find and change this in the `main.py` file to whatever.

---

## Testing

### Running Unit Tests
Unit tests are located in the `test/` directory. To run them, use:
```bash
python -m unittest discover -s test -p "*.py"
```

The tests cover:
- Environment variable validation.
- JSON file parsing and song grouping.
- Exception handling for missing environment variables.

---

## File Structure
```plaintext
project_root/
├── data/
│   └── songs.json            # Your input file with song data
├── src/
│   └── main.py               # Main script
├── test/
│   └── test_main.py          # Unit tests
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Handling Spotify Rate Limits
The application automatically handles Spotify's rate-limiting (HTTP 429 responses). When rate-limited, the app will:
1. Pause execution based on the `Retry-After` header from Spotify.
2. Retry the API call after the specified delay.

---

## Example Output
When the script runs successfully, you will see output similar to:
```plaintext
Created playlist: Triple J Top 100 1996
Song not found: Missing Song by Artist Name
Playlist 'Triple J Top 100 1996' created successfully!
```

---

## Troubleshooting
1. **Environment Variables Not Set**
   - Ensure `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REDIRECT_URI` are set in your environment.

2. **Songs Not Found**
   - If a song is missing from Spotify, it will be logged in the output.

3. **Authentication Issues**
   - Ensure your `SPOTIFY_REDIRECT_URI` matches the URI registered in your Spotify developer dashboard.

---

## License
This project is licensed under the GLWTS Public License - see the [LICENSE](LICENSE.md) file for details

---

## Acknowledgments
- [Spotipy](https://github.com/plamere/spotipy): Python client library for Spotify Web API.  
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/): For enabling playlist creation and song search.

---

