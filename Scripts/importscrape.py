#!/usr/bin/env python3

# This script takes the newlinejson file created by Scripts/workout_scraper.py
# and puts the data into our database's exercises table.

# import newlinejson as nlj
import json
import requests

db = 'http://138.197.49.155:8000/api/database/'
dbKey = 'SoftCon2018'
jFile = 'Logs/exercises.json'

with open(jFile) as src:
    i = 0
    for line in src:
        # Load our json object from a line in the nlj file
        o = json.loads(line)

        # Parse that json object into our fields
        _id         = i
        _name       = json.dumps(o["exercise_name"])
        _duration   = 0
        _type       = json.dumps(o["type"])
        _muscle     = json.dumps(o["main_muscle_worked"])
        _equipment  = json.dumps(o["equipment"])
        _level      = json.dumps(o["level"])
        _images     = json.dumps(o["associated_images"])
        _guide      = json.dumps(o["guide"])

        # Index the exercise id
        i += 1

        # Insert Fields into our Database's exercises Table
        print("id: %d name: %s" % (_id, _name))
        r = requests.post(db, data = {'key': dbKey, \
            'query': 'INSERT INTO exercises (id, name, duration, type, muscle, equipment, level) ' \
                    + 'VALUES (%d, %s, %10.5f, %s, %s, %s, %s)' \
                    % (_id, _name, _duration, _type, _muscle, _equipment, _level)})

        # r = requests.post(db, data = {'key': dbKey, \
        #     'query': 'INSERT INTO exercises (id, name, duration, type, muscle, equipment, level, images, guide) ' \
        #             + 'VALUES (%d, %s, %10.5f, %s, %s, %s, %s, %s, %s)' \
        #             % (_id, _name, _duration, _type, _muscle, _equipment, _level, _images, _guide)})
        print(r.json()["Status"])
