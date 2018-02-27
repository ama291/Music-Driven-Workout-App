#testrequest.py
import requests

# Make request to API
# dbURL = 'http://138.197.49.155:5000/api/database/'
# query = 'select bpm from exercises limit 5'
# key = 'SoftCon2018'
# r = requests.post(dbURL, data = {'query': query, 'key': key})
# print(r.json())


def getBPM(rpm,category):
    if category == "Cardio":
        max_beats = 170
    if category == "Powerlifting":
        max_beats =140
    if category == "Strongman":
        max_beats = 140
    if category == "Olympic Weightlifting":
        max_beats = 140
    if category == "Strength":
        max_beats = 140
    if category == "Plyometrics":
        max_beats = 150
    if category == "Stretching":
        max_beats = 80

    bpm = rpm
    n = 1
    while bpm <= max_beats:
        if rpm*(2*n) <= max_beats:
            bpm = rpm*(2*n)
            n = n+1
        else:
            break

    return bpm

def bpm_database():

    query = 'SELECT id FROM exercises'
    r = requests.post('http://138.197.49.155:5000/api/database/',
                          data={'query': query, 'key': 'SoftCon2018'})
    ids = [i[0] for i in r.json()["Result"]]
    for id in ids:
        print(id)
        query = 'SELECT rpm,type FROM exercises where id = %d' %(id)
        r = requests.post('http://138.197.49.155:5000/api/database/',
                          data={'query': query, 'key': 'SoftCon2018'})
        if r.json()["Status"] == "Success" and len(r.json()["Result"]) > 0:
            rpm = r.json()["Result"][0][0]
            category = r.json()["Result"][0][1]
            query = 'UPDATE exercises SET bpm = %d where id = %d' %(getBPM(rpm,category),id)
            r = requests.post('http://138.197.49.155:5000/api/database/',
                              data={'query': query, 'key': 'SoftCon2018'})
            #print(r.json()["Status"])

#bpm_database()


dbURL = 'http://138.197.49.155:5000/api/database/'
query = 'select rpm, bpm, type from exercises order by RANDOM() limit 10'
key = 'SoftCon2018'
r = requests.post(dbURL, data = {'query': query, 'key': key})
res = r.json()["Result"]
for i in range(len(res)):
    print("rpm", res[i][0], "bpm", res[i][1], "category", res[i][2])
