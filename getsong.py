import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Setel credential aplikasi Spotify Anda
client_id = '529a5b95ad974ff68fccd1e2cbd8b404'
client_secret = '9b95a933b31e4d4a8cac7b8729265b7d'

# Inisialisasi objek Spotipy
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Ambil URI playlist Spotify
playlist_uri = 'https://open.spotify.com/playlist/37i9dQZF1DWZxM58TRkuqg?si=9b28154c9a994b39'

# Ambil data playlist
playlist = sp.playlist(playlist_uri)

# list untuk menyimpan judul, artis dari playlist
songs = []

# Loop melalui lagu-lagu dalam playlist
for track in playlist['tracks']['items']:
    track_name = track['track']['name']
    artist_name = track['track']['artists'][0]['name']
    songs.append({"title": track_name, "artist": artist_name})

with open('songs.json', 'w') as json_file:
    json.dump(songs, json_file)

with open('songs.json', 'r') as json_file:
    songs = json.load(json_file)

# Menampilkan isi file dengan format yang lebih rapi
print(json.dumps(songs, indent=4))
print(len(songs))
