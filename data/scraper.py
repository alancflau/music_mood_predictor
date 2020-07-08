import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import requests
import time
import pandas as pd

def datascrape(user_id = 'spotify', playlist_id = None, sp = None):
    
    # music metadata
    results = sp.user_playlist(user_id, playlist_id, 'tracks')
    
    playlist_tracks_data = results['tracks']
    playlist_tracks_id = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []
    
    for track in playlist_tracks_data['items']:
        playlist_tracks_id.append(track['track']['id'])
        playlist_tracks_titles.append(track['track']['name'])

        # retrieve artist names
        artist_list = []
        for artist in track['track']['artists']:
            artist_list.append(artist['name'])

        playlist_tracks_artists.append(artist_list)
        playlist_tracks_first_artists.append(artist_list[0])
    
    
    # music features
    features = sp.audio_features(playlist_tracks_id)
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    
    features_df['title'] = playlist_tracks_titles
    features_df['first_artist'] = playlist_tracks_first_artists
    features_df['all_artists'] = playlist_tracks_artists
    #features_df = features_df.set_index('id')
    features_df = features_df[['title', 'first_artist', 'all_artists', 'id',
                               'danceability', 'energy', 'key', 'loudness',
                               'mode', 'acousticness', 'instrumentalness',
                               'liveness', 'valence', 'tempo',
                               'duration_ms', 'time_signature']]

    return features_df

