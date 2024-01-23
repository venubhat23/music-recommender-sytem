from flask import Flask, render_template, request
import pickle
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

app = Flask(__name__)

CLIENT_ID = "7dc5af9e03dc436fb9f9da3023c2909f"
CLIENT_SECRET = "a023a98dea6e4128aac3f5a972268ba7"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load pickled data
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names,recommended_music_posters


@app.route('/')
def index():
    music_list = music['song'].values
    return render_template('index.html', music_list=music_list)


@app.route('/recommendation', methods=['POST'])
def recommendation():
    selected_song = request.form['selected_song']
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    return render_template('recommendation.html', names_and_posters=zip(recommended_music_names, recommended_music_posters))


if __name__ == '__main__':
    app.run(debug=True)
