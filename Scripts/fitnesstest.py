import requests
from random import randint
from Scripts.log import Log
import json
from datetime import datetime

dbURL = "http://138.197.49.155:8000/api/database/"
key = "SoftCon2018"

def countExercises(category):
    query = "SELECT count(*) FROM exercises WHERE type = '%s'" % category
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    if r.status_code != requests.codes.ok:
        return -1
    return r.json()["Result"][0][0]

## My test
# print(countExercises("Strength"))

def getExQuery(categories):
    string = "SELECT * FROM exercises WHERE "
    for cat in categories:
        string += "type = '%s' OR " % cat
    string = string[:-4]
    return string

## My test
# print(getExQuery(["Strength"]))

## Add route
def getTrackedExercises(userID):
    """
    returns a list of exercises
    """
    query = "SELECT * FROM userexercises WHERE userID = %d" % userID
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    if r.status_code != requests.codes.ok:
        #TODO
        return
    res = r.json()["Result"]
    exercises = []
    IDs = []
    for i in res:
        if i[0] not in IDs:
            query = "SELECT * FROM exercises WHERE id = %d" % i[0]
            r = requests.post(dbURL, data = {'query':query, 'key':key})
            if r.status_code != requests.codes.ok:
                #TODO
                return
            print(r.json())
            ex = r.json()["Result"]
            exercises.append(ex)
            IDs.append(i[0])
    return exercises

## My test
# getTrackedExercises(1)

def getUntrackedIDs(categories, numUntracked, trackedIDs):
    query = getExQuery(categories)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    if r.status_code != requests.codes.ok:
        ##TODO
        return
    res = r.json()["Result"]
    num = len(res)
    untrackedIDs = []
    count = 0
    while len(untrackedIDs) < numUntracked and count < num:
        i = randint(0,num)
        ID = res[i][0]
        if ID not in trackedIDs:
            untrackedIDs.append(ID)
        count += 1
    if len(untrackedIDs) < numUntracked:
        #TODO
        pass
    return untrackedIDs

## My test
# print(getUntrackedIDs(["Strength"], 5, [412, 567]))

## Add route
## This is slow. We should make it faster
def getFitnessTest(categories, numExercises, trackedIDs):
    numUntracked = numExercises - len(trackedIDs)    
    untrackedIDs = getUntrackedIDs(categories, numUntracked, trackedIDs)
    exerciseIDs = trackedIDs + untrackedIDs
    assert len(exerciseIDs) == numExercises
    exercises = []
    for ID in exerciseIDs:
        query = "SELECT * FROM exercises WHERE id = %d" % ID
        r = requests.post(dbURL, data = {'query':query, 'key':key})
        if r.status_code == requests.codes.ok and len(r.json()["Result"]) == 1:
            exercises.append(r.json()["Result"][0])
        else:
            #TODO
            pass
    assert len(exercises) == numExercises
    return exercises

## My test
# print(getFitnessTest(["Strength"], 3, [4]))

def checkTracked(userID, exID): 
    query = "SELECT * FROM userexercises WHERE userID = %s AND exID = %s" % (userID, exID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    if r.status_code != requests.codes.ok or "Result" not in r.json():
        #TODO
        return False
    res = r.json()["Result"]
    if len(res) == 0:
        return False
    elif res[0][5] == 1: ##tracked bit
        return True
    return False

## My test
# print(checkTracked(1,12))

## Add route
def isTracked(userID, exID):
    return str(checkTracked(userID, exID))

def addExercise(userID, exID, timestamp, rate):
    ct = checkTracked(userID, exID)
    if ct == True:
        trackBit = 1
    else:
        trackBit = 0
    query = "INSERT INTO userexercises \
     (userID, exID, timestamp, rate, tracked) \
     VALUES (%d,%d,'%s',%f,%d)" % \
     (userID, exID, timestamp, rate, trackBit)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    if r.status_code != requests.codes.ok:
        #TODO
        pass
    return "OK" ## not sure about this

## AddRoute
def processMotionData(userID, exID, timestamp, rawdata):
    log = Log(rawdata, data=True)
    rate = log.getFrequency()
    addExercise(userID, exID, timestamp, rate)
    return rate

## My test:
# with open("Logs/log1.json") as f:
#     data = json.load(f)
# print(processMotionData(1,12, "2012-12-12 12:12:12",data))

## Add route
def toggleTracked(userID, exID, clear=False):
    if clear:
        trackBit = 0
    else:
        tracked = checkTracked(userID, exID)
    trackBit = 1 - tracked
    query = "UPDATE userexercises SET tracked = %d WHERE userID = '%s' AND exID = '%s'" % (trackBit, userID, exID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    if r.status_code != requests.codes.ok:
        #TODO
        pass
    return [userID, exID, trackBit]

## My test:
# print(toggleTracked(1, 12))

