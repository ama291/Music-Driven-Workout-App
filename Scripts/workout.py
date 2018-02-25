#!/usr/bin/env python3
import uuid
import requests
import random
from Scripts.exercise import Exercise
from Scripts.dbfunctions import testDB, realDB
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

dbURL = realDB
clientID = '8f81031574b54170a24a3a1afab27578'
clientSecret = '0c0f604c8a564aafa1bfb49325eb0f76'
redirectURL = 'https://example.com/callback/'
client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class Workout(object):
    def __init__(self, uid, spotID, themes, categories, muscleGroups, equipment, duration, difficulty, accessToken):
        self.ID = str(uuid.uuid4())  # random UUID, jsonpickle has strings for dict keys
        self.themes = themes # for music recommendations
        self.uid = uid # user ID, to get fitness test info
        self.spotID = spotID # spotify ID, for accessing spotify info
        self.accessToken = accessToken # for authenticated spotify requests
        self.categories = categories
        self.muscleGroups = muscleGroups
        self.equipment = equipment
        self.equipment.append("Body Only") # Body Only is always included in list of equipment
        self.duration = duration # updated by generateWorkout
        self.difficulty = difficulty
        self.Exercises = [] # filled by generateWorkout
        self.currExercise = 0 # index of current exercise

    def setCurrEx(self, idx):
        self.currExercise = idx


    def generateWorkout(self):
        limit = 30 # number of exercises for each trial, can be tuned
        trials = 10 # number of runs of algorithm, can be tuned
        results = [[]] * trials
        # TODO - need to add bpm column to exercise table
        attributes = ['id', 'name', 'type', 'muscle', 'level', 'equipment',
                        'range_start', 'range_end', 'increment', 'rpm', 'images'] # TODO - add 'bpm'
        equipment = ', '.join("\'" + e + "\'" for e in self.equipment)

        duration = self.duration
        difficulty = "\'" + self.difficulty + "\'"
        if self.categories is not None: # category option
            categories = ', '.join("\'" + c + "\'" for c in self.categories)

            query = 'SELECT %s FROM exercises WHERE type IN (%s) AND equipment IN (%s) \
                    AND range_start <= %d AND level = %s ORDER BY RANDOM() LIMIT %d' \
                    % (', '.join(attributes), categories, equipment, duration, difficulty, limit)

            # get random subset of exercises from query for each trial
            for i in range(trials):

                r = requests.post(dbURL,
                    data={'query': query, 'key': 'SoftCon2018'})

                if r.json()['Status'] != 'Success':
                    return False
                results[i] = r.json()['Result']

        else: # muscleGroup option
            muscleGroups = ', '.join("\'" + m + "\'" for m in self.muscleGroups)

            query = 'SELECT %s FROM exercises WHERE muscle IN (%s) AND equipment \
                    IN (%s) AND range_start <= %d AND level = %s ORDER BY RANDOM() LIMIT %d' \
                    % (', '.join(attributes), muscleGroups, equipment, duration, difficulty, limit)

            # get random subset of exercises from query for each trial
            for i in range(trials):

                r = requests.post(dbURL,
                    data={'query': query, 'key': 'SoftCon2018'})

                if r.json()['Status'] != 'Success':
                    return False
                results[i] = r.json()['Result']


        """ run the algorithm multiple times (based on trials),
        greedily choose the closest outcome, each trial has a
        random subset of the exercises returned by that query """

        best = 0
        finalExercises = []
        for i in range(trials):
            dur, exercises = self.pickExercises(results[i], attributes)
            if dur > best:
                best, finalExercises = dur, exercises
            if best == self.duration:
                break

        self.duration = best
        self.Exercises = finalExercises

        for ex in self.Exercises:
            # update rpm/bpm if user has tested on the exercise
            # TODO - will also need to remap bpm
            query = 'select rate from userexercises where exID = %d and timestamp \
             = (select max(timestamp) from userexercises where exID = %d) limit 1' % (ex.id, ex.id)
            r = requests.post(dbURL,
                              data={'query': query, 'key': 'SoftCon2018'})
            if r.json()["Status"] == "Success" and len(r.json()["Result"]) > 0:
                scale = 0.9 if self.difficulty == "Intermediate" else 0.7
                ex.rpm = scale * r.json()["Result"][0][0]
                # TODO - ex.bpm =

            # get recommendations based on bpm, with duration >= to exercise duration
            ex.tracks = self.getRecommendations(self.spotID, self.themes, self.accessToken, ex.bpm, ex.duration)

        return True


    def pickExercises(self, dbExercises, ordering):
        m, n = len(dbExercises), len(ordering)
        exercises = []
        total_duration = 0

        # add in exercises as long as they do not put over self.duration
        for i in range(m):
            exRange = [0]*2
            for j in range(n):
                if ordering[j] == "id":
                    id = dbExercises[i][j]
                elif ordering[j] == "name":
                    name = dbExercises[i][j]
                elif ordering[j] == "level":
                    difficulty = dbExercises[i][j]
                elif ordering[j] == "type":
                    category = dbExercises[i][j]
                elif ordering[j] == "muscle":
                    muscleGroup = dbExercises[i][j]
                elif ordering[j] == "equipment":
                    equipment = dbExercises[i][j]
                elif ordering[j] == "images":
                    images = dbExercises[i][j]
                elif ordering[j] == "range_start":
                    exRange[0]= dbExercises[i][j]
                elif ordering[j] == "range_end":
                    exRange[1] = dbExercises[i][j]
                elif ordering[j] == "increment":
                    increment = dbExercises[i][j]
                elif ordering[j] == "rpm":
                    rpm = dbExercises[i][j]
                # else: # bpm
                    # bpm = dbExercises[i][j]

            # TODO - update with real bpm
            new = Exercise(id, name, difficulty, category, muscleGroup, equipment, images, exRange, increment, rpm, 120 + 10*i)

            if new.duration + total_duration <= self.duration:
                exercises.append(new)
                total_duration += new.duration
                if total_duration == self.duration:
                    break

        return total_duration, exercises


    def getRecommendations(self, spotID, themes, accessToken, tempo, duration):
        # generate seeds (either using the given themes or the user's spotify data)
        seeds = self.getSeeds(spotID, themes, accessToken)

        # get recommendations based on those seeds
        recs = sp.recommendations(seed_artists=seeds['artists'], seed_genres=seeds['genres'],
                                         seed_tracks=seeds['tracks'], limit=30, target_tempo=tempo)['tracks']

        # add tracks until summed duration >= exercise duration
        tracks = []
        total_duration = 0
        for r in recs:
            dur = r['duration_ms'] / (1000 * 60) # duration of this song in minutes

            if total_duration < duration:
                tracks.append(r['uri'])
                total_duration += dur
            if total_duration >= duration:
                break

        return tracks


    def getSeeds(self, spotID, themes, accessToken):

        seed_artists = []
        seed_tracks = []
        seed_genres = []

        # if themes chosen, use those
        if themes is not None:
            for theme in themes:
                if theme.theme == 'artist':
                    seed_artists.append(theme.spotifyId)
                elif theme.theme == 'track':
                    seed_tracks.append(theme.spotifyId)
                else:
                    seed_genres.append(theme.spotifyId)
        else:
            # first check if user has workout playlists
            playlists = self.getUserWorkoutPlaylists(spotID, accessToken)

            if len(playlists) > 0:
                # pick a random playlist
                idx = random.randint(0, len(playlists) - 1)
                p = playlists[idx]
            else: # get workout category playlists
                playlists = self.getWorkoutCategoryPlaylists() # TODO - make this call once, add as param
                # pick a random playlist
                idx = random.randint(0, len(playlists) - 1)
                p = playlists[idx]

            # get the playlists tracks
            p_tracks = self.getPlaylistTracks(p['owner'], p['id'])
            num_tracks = len(p_tracks)

            # set up to 3 artists
            subset1 = random.sample(p_tracks, min(3, num_tracks))
            seed_artists = [t['track']['artists'][0]['id'] for t in subset1]

            # set up to 2 tracks
            subset2 = random.sample(p_tracks, min(2, num_tracks))
            seed_tracks = [t['track']['id'] for t in subset2]

        seed_artists = seed_artists if len(seed_artists) > 0 else None
        seed_tracks = seed_tracks if len(seed_tracks) > 0 else None
        seed_genres = seed_genres if len(seed_genres) > 0 else None
        return {'artists': seed_artists, 'tracks': seed_tracks, 'genres': seed_genres}


    def getUserWorkoutPlaylists(self, spotID, accessToken):
        # TODO - change to current user playlists
        # sp = spotipy.Spotify(auth=accessToken)
        # sp.trace = False
        # results = sp.current_user_playlists(limit=20)

        results = sp.user_playlists(spotID, limit=20)
        playlists = [{'name': p['name'], 'id': p['id'], 'owner': p['owner']['id']} for p in results['items']]
        while results['next']:
            results = sp.next(results)
            playlists.extend([{'name': p['name'], 'id': p['id'], 'owner': p['owner']['id']} for p in results['items']])
        # filter playlists that have 'workout' or 'Workout' in the name
        playlists = list(filter(lambda p: 'workout' in p['name'] or 'Workout' in p['name'], playlists))
        return playlists


    def getWorkoutCategoryPlaylists(self):
        # get workout category playlists
        results = sp.category_playlists(category_id='workout')['playlists']
        playlists = [{'id': p['id'], 'owner': p['owner']['id']} for p in results['items']]
        while results['next']:
            results = sp.next(results)['playlists']
            playlists.extend([{'id': p['id'], 'owner': p['owner']['id']} for p in results['items']])
        return playlists


    def getPlaylistTracks(self, owner, pid):
        fields = 'next,items(track(id,artists(id)))'
        results = sp.user_playlist_tracks(owner, playlist_id=pid, fields=fields, limit=50)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        return tracks



    # TODO - implement this
    def getBPM(self,rpm,min_beats,max_beats):
        #return bpm int
        return[]
