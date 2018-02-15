#!/usr/bin/env python3
import uuid
import requests
from Scripts.exercise import Exercise
#from Scripts.userexercise import UserExercise
class Workout(object):
    def __init__(self, uid, themes, categories, muscleGroups, equipment, duration, difficulty):
        self.ID = str(uuid.uuid4())  # random UUID, jsonpickle has strings for dict keys
        self.themes = themes # will not be used until iter 2, for music recommendations
        self.uid = uid # user ID, to get fitness test info
        self.categories = categories
        self.muscleGroups = muscleGroups
        self.equipment = equipment
        self.equipment.append("Body Only") #Body Only is always included in list of equipment
        self.duration = duration # updated by generateWorkout
        self.difficulty = difficulty
        #self.difficulty
        self.Exercises = [] # filled by generateWorkout
        self.currExercise = 0 # index of current exercise

    def setCurrEx(self, idx):
        self.currExercise = idx

    def generateWorkout(self):
        limit = 40 # number of exercises for each trial, can be tuned
        trials = 5 # number of runs of algorithm, can be tuned
        results = [[]] * trials
        attributes = ['name', 'type', 'muscle', 'level', 'equipment',
                        'range_start', 'range_end', 'increment', 'rpm']
        equipment = ', '.join("\'" + e + "\'" for e in self.equipment)

        duration = self.duration
        difficulty = "\'" + self.difficulty + "\'"
        if self.categories is not None: # category option
            categories = ', '.join("\'" + c + "\'" for c in self.categories)

            query = 'SELECT %s FROM exercises WHERE type IN (%s) AND equipment IN (%s) \
                    AND range_start <= %s AND level = %s ORDER BY RANDOM() LIMIT %s' \
                    % (', '.join(attributes), categories, equipment, duration, difficulty, str(limit))
            
            for i in range(trials):

                r = requests.post('http://138.197.49.155:8000/api/database/',
                    data={'query': query, 'key': 'SoftCon2018'})
                
                print(r.json()['Status'])
                if r.json()['Status'] != 'Success':
                    return False
                results[i] = r.json()['Result']

        else: # muscleGroup option
            muscleGroups = ', '.join("\'" + m + "\'" for m in self.muscleGroups)

            query = 'SELECT %s FROM exercises WHERE muscle IN (%s) AND equipment \
                    IN (%s) AND range_start <= %s AND level = %s ORDER BY RANDOM() LIMIT %s' \
                    % (', '.join(attributes), muscleGroups, equipment, duration, difficulty, str(limit))

            for i in range(trials):
                
                r = requests.post('http://138.197.49.155:8000/api/database/',
                    data={'query': query, 'key': 'SoftCon2018'})
                
                print(r.json()['Status'])

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
                print('reset best on iter' + str(i))
                best, finalExercises = dur, exercises
            if best == self.duration:
                break

        self.duration = best
        self.Exercises = finalExercises

        # TODO - if tested on, get rpm from user, scaled to difficulty
        return True


    def pickExercises(self, dbExercises, ordering):
        m, n = len(dbExercises), len(ordering)
        exercises = []
        total_duration = 0

        for i in range(m):
            exRange = [0]*2
            for j in range(n):
                if ordering[j] == "name":
                    name = dbExercises[i][j]
                elif ordering[j] == "level":
                    difficulty = dbExercises[i][j]
                elif ordering[j] == "type":
                    category = dbExercises[i][j]
                elif ordering[j] == "muscle":
                    muscleGroup = dbExercises[i][j]
                elif ordering[j] == "equipment":
                    equipment = dbExercises[i][j]
                elif ordering[j] == "range_start":
                    exRange[0]= dbExercises[i][j]
                elif ordering[j] == "range_end":
                    exRange[1] = dbExercises[i][j]
                elif ordering[j] == "increment":
                    increment = dbExercises[i][j]
                else: # ordering[j] == "rpm"
                    rpm = dbExercises[i][j]

            new = Exercise(id,name, difficulty, category, muscleGroup, equipment, [], exRange, increment, rpm)

            if new.duration + total_duration <= self.duration:
                exercises.append(new)
                total_duration += new.duration
                if total_duration == self.duration:
                    break

        return total_duration, exercises
