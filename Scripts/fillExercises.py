import requests
import random

categories = ["Cardio", "Olympic Weightlifting", "Plyometrics",
              "Powerlifting", "Strength", "Stretching", "Strongman"]

range_start = [(10,20), (2,3) ,(2,4), (2, 3), (2, 4), (1, 2), (2, 3)]
range_end = [(30,40), (4,5), (8,10), (4,5), (8,10), (3,4), (4,5)]
increment = [5, 0.5, 1, 0.5, 1, 0.5, 0.5]
rpm = [(40,80,4), (2,4,1), (10,30,2), (4,8,2), (10,15,1), (2,4,1), (2,4,1)]

for i in range(len(categories)):
    print(categories[i])
    c = "\'" + categories[i] + "\'"
    inc = str(increment[i])

    query = 'SELECT id FROM exercises WHERE type = %s' % c
    r = requests.post('http://138.197.49.155:8000/api/database/',
                      data={'query': query, 'key': 'SoftCon2018'})
    result = r.json()["Result"]
    for j in range(len(result)):
        id = str(result[j][0])
        rs = str(random.randint(range_start[i][0], range_start[i][1]))
        re = str(random.randint(range_end[i][0], range_end[i][1]))
        rep = str(random.randrange(rpm[i][0], rpm[i][1], rpm[i][2]))
        query = 'update exercises set range_start = %s, range_end = %s, \
                rpm = %s, increment = %s where id = %s' % (rs, re, rep, inc, id)
        r = requests.post('http://138.197.49.155:8000/api/database/',
                          data={'query': query, 'key': 'SoftCon2018'})
        if r.json()['Status'] != "Success":
            print("error")
            break