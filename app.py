import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "529a5b95ad974ff68fccd1e2cbd8b404"
CLIENT_SECRET = "9b95a933b31e4d4a8cac7b8729265b7d"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://www.hypebot.com/wp-content/uploads/2019/11/spotify-1759471_1920.jpg"

def recommend(song):
    index = music[music['title'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    track_id = []
    for i in distances[1:11]:
        # fetch the music poster
        artist = music.iloc[i[0]].artist
        id = music.iloc[i[0]].track_id
        print(artist)
        print(id)
        print(music.iloc[i[0]].title)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].title, artist))
        recommended_music_names.append(music.iloc[i[0]].title)
        track_id.append(music.iloc[i[0]].track_id)

    return recommended_music_names,recommended_music_posters, track_id

st.header('Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('combined_similarity.pkl','rb'))

music_list = music['title'].values
selected_music = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

button_style = """
    background-color: #4CAF50;
    color: white;
    padding: 10px 24px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 10px;
"""
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters, track_id = recommend(selected_music)
    
    # Jumlah kolom dalam satu baris
    cols_per_row = 5
    
    # Menghitung jumlah baris yang dibutuhkan
    num_rows = (len(recommended_music_names) + cols_per_row - 1) // cols_per_row
    
    # Looping melalui setiap baris
    for row in range(num_rows):
        cols = st.columns(cols_per_row)
        
        # Looping melalui setiap kolom dalam baris tersebut
        for col_index in range(cols_per_row):
            item_index = row * cols_per_row + col_index
            if item_index < len(recommended_music_names):
                with cols[col_index]:
                    st.text(recommended_music_names[item_index])
                    st.image(recommended_music_posters[item_index])
                    st.markdown(f'<a href="https://open.spotify.com/track/{track_id[item_index]}" target="_blank"><button style="{button_style}">Play on Spotify</button></a>', unsafe_allow_html=True)
