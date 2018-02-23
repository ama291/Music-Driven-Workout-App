#!/usr/bin/env python3
import uuid
import requests
from Scripts.exercise import Exercise
from Scripts.dbfunctions import testDB, realDB

dbURL = realDB

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
                        'range_start', 'range_end', 'increment', 'rpm', 'images'] # add 'bpm'
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

            new = Exercise(id, name, difficulty, category, muscleGroup, equipment, images, exRange, increment, rpm, 120)

            if new.duration + total_duration <= self.duration:
                exercises.append(new)
                total_duration += new.duration
                if total_duration == self.duration:
                    break

        return total_duration, exercises

    # TODO - implement this
    def getRecommendations(self, spotID, themes, accessToken, tempo, duration):
        # call helper function to generate seeds lists
        # call recommendations with seeds lists
        # add exercises in until >= duration
        # return list of {name: , uri: , duration: } dicts
        return []

    # TODO - implement this
    def getSeeds(self, spotID, themes, accessToken):
        # return {tracks: , artists:, genres: } dict
        return []
