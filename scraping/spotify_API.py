import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import json

# spotify developerから取得したclient_idとclient_secretを入力
client_id = 'e76c88811ef9456eba51a877c24144b6'
client_secret = 'ccfa5e055e624ea194432bc19647b0cd'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTrackIDs(playlist_ids):
    track_ids = []
  
    for playlist_id in playlist_ids:
        playlist = sp.playlist(playlist_id)
        while playlist['tracks']['next']:
            for item in playlist['tracks']['items']:
                track = item['track']
                if not track['id'] in track_ids:
                    track_ids.append(track['id'])
            playlist['tracks'] = sp.next(playlist['tracks'])
        else:
            for item in playlist['tracks']['items']:
                track = item['track']
                if not track['id'] in track_ids:
                    track_ids.append(track['id'])
    return track_ids

playlist_ids = ["37i9dQZEVXbKqiTGXuCOsB"]  # SpotifyのプレイリストのIDを入力
track_ids = getTrackIDs(playlist_ids)
# print(len(track_ids))
# print(track_ids)

def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    name = meta['name']
    album = meta['album']['name']
    image = meta["album"]["images"][0]["url"]
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    key = features[0]['key']
    mode = features[0]['mode']
    danceability = features[0]['danceability']
    acousticness = features[0]['acousticness']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    valence = features[0]['valence']

    track = [name, album, artist, image, release_date, length, popularity, key, mode, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence]
    return track

tracks = []

for track_id in track_ids:
  time.sleep(0.5)
  track = getTrackFeatures(track_id)
  tracks.append(track)

#csvファイルを作るなら下の部分を使う
df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'image', 'release_date', 'length', 'popularity', 'key', 'mode', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'valence'])
df.head()
df.to_csv('Japan_Top50.csv', encoding='utf_8_sig')


# #jsonファイルを作るなら下の部分を使う
# items = ['name', 'album', 'artist', 'image', 'release_date', 'length', 'popularity', 'key', 'mode', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'valence']
# tracks_dict = {i+1: dict(zip(items,tracks[i])) for i in range(len(tracks))}
# # print(tracks_dict) これは試験用

# #ファイルごとに名前を変える
# with open("Japan_BEST2021.json","w") as f:
#     json.dump(tracks_dict,f,ensure_ascii=False, indent=4)