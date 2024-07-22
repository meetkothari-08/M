from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import random

# Initialize Flask app
app = Flask(__name__)

# Spotify API credentials
SPOTIPY_CLIENT_ID = '153c24e3b27d4839a6276cbe190acf74'
SPOTIPY_CLIENT_SECRET = 'bfdf5a9e308b41319df579131277b536'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Initialize Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-library-read'))

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('query')
    
    try:
        # Search for the query on Spotify
        results = sp.search(q=query, type='track', limit=10)
        
        # Extract track information from the search results
        tracks = results['tracks']['items']
        
        return render_template('search_results.html', tracks=tracks, query=query)
    
    except SpotifyException as e:
        return render_template('error.html', error_message=str(e))

# Route for receiving user input and showing recommendations
# Route for receiving user input and showing recommendations
# Route for receiving user input and showing recommendations
@app.route('/recommendations', methods=['POST'])
def recommendations():
    try:
        # Get popular tracks or curated playlists from Spotify
        recommended_tracks = sp.featured_playlists(limit=10)['playlists']['items']
        recommended_playlists = [playlist['name'] for playlist in recommended_tracks]
        
        # Remove duplicates from recommended playlists
        unique_playlists = []
        seen = set()
        for playlist in recommended_playlists:
            if playlist not in seen:
                unique_playlists.append(playlist)
                seen.add(playlist)
        
        return render_template('recommendations.html', recommended_playlists=unique_playlists)
    
    except SpotifyException as e:
        return render_template('error.html', error_message=str(e))


# Route for handling user favorites
@app.route('/favorites')
def favorites():
    try:
        # Get user's saved tracks
        saved_tracks = sp.current_user_saved_tracks()
        favorite_songs = [track['track']['name'] for track in saved_tracks['items']]
        
        return render_template('favorites.html', favorite_songs=favorite_songs)
    
    except SpotifyException as e:
        return render_template('error.html', error_message=str(e))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
