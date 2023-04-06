from dotenv import load_dotenv
import spotipy
import spotipy.util as util

load_dotenv()

client_id = 'your-client-id' #use your own client id
client_secret = 'your-client-secret' #use your own client secret
redirect_uri = 'your-redirect-uri' #use your own redirect uri
username = "your-username" #implement your spotify username
scope = "user-library-read playlist-modify-private"

auth_token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

sp = spotipy.Spotify(auth=auth_token)

def create_playlist(name, track_uris):
    '''
    This method creates a playlist
    '''
    playlist = sp.user_playlist_create(username, name, public=False)
    sp.user_playlist_add_tracks(username, playlist['id'], track_uris)
    return playlist

def find_tracks(mood, genres, vocal, popularity, billboard, artist_popularity):
    '''
    This method finds tracks for a user based on certain arguments given
    '''
    #Different moods which could've been inputted
    if mood == "happiness":
        mood_param = "valence:0.75-1.0 "
    elif mood == "contentment":
        mood_param = "valence:0.5-0.75 "
    elif mood == "sadness":
        mood_param = "valence:0.0-0.25 "
    elif mood == "melancholy":
        mood_param = "valence:0.25-0.5 "
    elif mood == "anger":
        mood_param = "energy:0.75-1.0 valence:0.5-0.75 "
    elif mood == "aggression":
        mood_param = "energy:0.75-1.0 valence:0.0-0.25 "
    elif mood == "tension":
        mood_param = "energy:0.75-1.0 valence:0.25-0.5 "
    elif mood == "relaxation":
        mood_param = "energy:0.0-0.25 valence:0.5-0.75 "
    elif mood == "boredom":
        mood_param = "energy:0.0-0.25 valence:0.0-0.25 "
    elif mood == "excitement":
        mood_param = "energy:0.75-1.0 valence:0.75-1.0 "
    mood_param = mood
    genre_list = ' '.join(['genre: ' + genre for genre in genres])
    vocals = 'vocal:' + vocal
    billboards = 'billboard:' + billboard
    popularity_range = f'popularity:{popularity}'
    query = mood_param + "AND" + genre_list + 'AND' + vocals + 'AND' + billboards + "AND" + popularity_range + 'AND' + artist_popularity
    results = sp.search(q=query, type='track', limit=50, market='US')
    tracks = results['tracks']['items']
    track_uris = []
    for track in tracks:
        track_uris.append(track['uri'])
    return track_uris

mood = input('What mood are you in (happiness, contentment, sadness, melancholy, anger, aggression, tension, relaxation, boredom, excitement) ')
genres = input('What genre would you like? Input a few if needed with commas: ')
vocals = input('Would you like the song to have vocals? (true, false) ')
popularity = input('How popular would you like the songs to be? (0-100) ')
billboard = input('Would you have liked the songs to be on billboard charts before? (true, false) ')
artist_popularity = input('How popular would you like the artists to be? (0-100) ')
if genres.find(','):
    genres = genres.split(',')
    for genre in genres:
        genre.strip()
tracks = find_tracks(mood = mood, genres = genres, vocal = vocals, popularity = popularity, billboard = billboard, artist_popularity=artist_popularity)
name = input('Give a name for your playlist: ')
playlist = create_playlist(name=name, track_uris=tracks)
print('Created playlist:', playlist['external_urls']['spotify'])