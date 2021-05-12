# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:18:02 2021

@author: Shrinidhi KR
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from fuzzywuzzy import fuzz
import pandas as pd
import math

def CreatePlaylist(username):
    # Create Appropriately Titled Empty Playlist For Samples
    playlist_name = f"All time favourites"    
    sp.user_playlist_create(username, name=playlist_name)
    print("Playlist Created.")
    return playlist_name

def GetPlaylistID(username, playlist_name):
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist['id']
    print("Got Playlist ID.")
    return playlist_id

def GetTrackIDs(sample_data, titles):
    #Get Spotify track ids for samples
    track_ids = []
    
    #Track Info Box Flow
    for i in range(len(sample_data)):
        results = sp.search(q=f"{sample_data['Song'][i]} {sample_data['Artist/Album'][i]} ", limit=5, type='track') #get 5 responses since first isn't always accurate
        if results['tracks']['total'] == 0: #if track isn't on spotify as queried, go to next track
            continue
        else:
            for j in range(len(results['tracks']['items'])):
                if fuzz.partial_ratio(results['tracks']['items'][j]['artists'][0]['name'], sample_data['Artist/Album'][i]) > 90 and fuzz.partial_ratio(results['tracks']['items'][j]['name'], sample_data['Song'][i]) > 90 : #get right response by matching on artist and title
                    track_ids.append(results['tracks']['items'][j]['id']) #append track id
                    break #don't want repeats of a sample ex: different versions
                else:
                    continue
    print('Got TrackIDs with fuzzy Artist and Song match')
    print('Lenght of Artist and Song TrackIDs {}'.format(len(track_ids)))
    
    #Track Annotation Flow
    annotation_track_ids = []
    for title in titles:
        results = sp.search(q=f"{title} ", type='track')
        if results['tracks']['total'] == 0: #if track isn't on spotify as queried, go to next track
            continue
        else:
            annotation_track_ids.append(results['tracks']['items'][0]['id'])
    
    print("Got TrackIDs with Song Title")
    print('Lenght of Song TrackIDs {}'.format(len(annotation_track_ids)))
        
    track_ids = track_ids + annotation_track_ids
    
    return track_ids


client_id = 'XXX'                   #get this from spotify developers site after registering/creating a spotify app
client_secret = 'XXX'
username = 'XXX'
scope = "playlist-modify-public"

token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri='http://localhost:8080') 
sp = spotipy.Spotify(auth=token)

sample_data = pd.read_csv('wynk_english_playlist.csv')
titles = sample_data['Song'].tolist()

playlist_name = CreatePlaylist(username)
track_ids = GetTrackIDs(sample_data, titles)
track_ids = list(dict.fromkeys(track_ids)) #remove duplicates
playlist_id = GetPlaylistID(username, playlist_name)

print('Lenght of final song list {}'.format(len(track_ids)))
itr = math.ceil(len(track_ids)/100) 

for i in range(itr):
    start = 100*i
    end = 100*(i+1)
    sp.user_playlist_add_tracks(username, playlist_id, track_ids[start:end])