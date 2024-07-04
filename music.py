import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import lyricsgenius
import os
import json

# Autentikasi dengan Spotify API
CLIENT_ID = "529a5b95ad974ff68fccd1e2cbd8b404"
CLIENT_SECRET = "9b95a933b31e4d4a8cac7b8729265b7d"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Inisialisasi Genius API
genius = lyricsgenius.Genius('JndC51J3t_O7pmCcOG5Ugj7bRbxB2mvmQMOg8uBIXfy7tl6AEO5oEZa62CgpC3ym')

# Daftar lagu dan artis yang ingin Anda cari
with open('songs.json', 'r') as json_file:
    songs = json.load(json_file)

# List untuk menyimpan hasil
results_list = []

# Mencari dan menganalisis setiap lagu dalam daftar
for song in songs:
    song_name = song["title"]
    artist_name = song["artist"]

    # Mencari lagu berdasarkan judul dan nama artis
    results = sp.search(q=f"track:{song_name} artist:{artist_name}", type='track', limit=1)

    if results and results["tracks"]["items"]:
        track_info = results["tracks"]["items"][0]
        song_title = track_info['name']
        artists = ', '.join(artist['name'] for artist in track_info['artists'])
        track_id = track_info['id']

        related_artists = track_info['artists']

        # Mencari lirik menggunakan Genius
        try:
            song_lyrics = genius.search_song(song_title, artist_name).lyrics
        except Exception as e:
            song_lyrics = ""  # Setel song_lyrics menjadi string kosong jika lirik tidak ditemukan

        # Menyimpan hasil dalam dictionary
        result = {
            'Judul Lagu': song_title,
            'Artis': artists,
            'Track ID': track_id,
            'Lirik': song_lyrics,
        }

        results_list.append(result)
    else:
        print(f"Lagu '{song_name}' oleh '{artist_name}' tidak ditemukan.")

# Membaca DataFrame yang ada (jika file CSV sudah ada)
existing_csv_filename = 'data.csv'

if os.path.exists(existing_csv_filename):
    existing_df = pd.read_csv(existing_csv_filename)
else:
    existing_df = pd.DataFrame()  # Buat DataFrame kosong jika file CSV belum ada

# Menambahkan hasil pencarian baru ke DataFrame jika data belum ada dalam DataFrame yang ada
for result in results_list:
    is_duplicate = existing_df[
        (existing_df['Judul Lagu'] == result['Judul Lagu']) & 
        (existing_df['Artis'] == result['Artis'])
    ]
    
    if is_duplicate.empty:
        existing_df = pd.concat([existing_df, pd.DataFrame([result])], ignore_index=True)

# Menyimpan DataFrame ke file CSV
existing_df.to_csv(existing_csv_filename, index=False)
print(existing_df)

