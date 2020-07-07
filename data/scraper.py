import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import requests
import time
import pandas as pd


def get_songs(userID, playlistID, sp):
    ids = []
    playlist = sp.user_playlist(userID, playlistID)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

def getTrackFeatures(id, sp):
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy,
             instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    
    return track


def get(ids, sp):
    # loop over track ids 
    tracks = []
    for i in range(len(ids)):
        time.sleep(1)
        track = getTrackFeatures(ids[i], sp)
        tracks.append(track)

    # create dataset
    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 
                                         'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 
                                         'speechiness', 'tempo', 'time_signature'])
    
    return df
    #df.to_csv("spotify.csv", sep = ',')