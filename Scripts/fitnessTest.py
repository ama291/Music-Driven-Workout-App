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


def getExQuery(categories):
    string = "SELECT * FROM exercises WHERE "
    for cat in categories:
        string += "type = '%s' OR " % cat
    string = string[:-4]
    return string


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
        if i[0] in IDs:
            continue
        query = "SELECT * FROM exercises WHERE id = %d" % i[2]
        r = requests.post(dbURL, data = {'query':query, 'key':key})
        if r.status_code != requests.codes.ok:
            #TODO
            return
        ex = r.json()["Result"][0]
        exercises.append(ex)
        IDs.append(i[0])
    return exercises


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

## Add route
def getPreviousResults(userID, exID):
    query = "SELECT * FROM userexercises WHERE userID = '%s' AND exID = %s" % (userID, exID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    if r.status_code != requests.codes.ok or "Result" not in r.json():
        #TODO
        return False
    res = r.json()["Result"]
    return res


## Add route
def checkTracked(userID, exID): 
    exs = getPreviousResults(userID, exID)
    if len(exs) == 0:
        return False
    elif exs[0][5] == 1: ##tracked bit
        return True
    return False


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
    return True


## Add route
def processMotionData(userID, exID, timestamp, rawdata):
    log = Log(rawdata, data=True)
    rate = log.getFrequency()
    addExercise(userID, exID, timestamp, rate)
    return rate


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

