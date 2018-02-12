#!/usr/bin/env python3

import newlinejson as nlj
import json
import requests

db = 'http://138.197.49.155:8000/api/database/'
dbKey = 'SoftCon2018'
nljFile = 'Logs/workoutScrape'

with nlj.open(nljFile) as src:
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
        requests.post(db, data = {'key': dbKey, \
            'query': 'INSERT INTO exercises (id, name, duration, type, muscle, equipment, level, images, guide) ' \
                      + '(%d, %s, %10.5f, %s, %s, %s, %s, %s, %s)' \
                      % (_id, _name, _duration, _type, _muscle, _equipment, _level, _images, _guide)})
