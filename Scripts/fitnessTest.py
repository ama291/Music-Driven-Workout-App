import requests
from random import randint
from Scripts.log import Log
import json
from datetime import datetime

dbURL = "http://138.197.49.155:5000/api/database/"
key = "SoftCon2018"
dbCategories = ["Cardio", "Olympic Weightlifting", "Plyometrics", "Powerlifting", "Strength", "Stretching", "Strongman"]

def countExercises(category):
    """
    return (integer): count exercises of a given category
    """
    query = "SELECT count(*) FROM exercises WHERE type = '%s'" % category
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return r.json()["Result"][0][0]


def getExQuery(categories):
    """
    return (string): the SQL query for selecting exercises from any of these
    categories
    """
    string = "SELECT * FROM exercises WHERE "
    for cat in categories:
        string += "type = '%s' OR " % cat
    string = string[:-4]
    return string

def getExerciseFromID(ID):
    """
    return (exercise entry from database): the exercise corresponding to that 
    ID
    """
    query = "SELECT * FROM exercises WHERE id = %d" % ID
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    ex = r.json()["Result"][0]
    return ex

## Add route
def getTrackedExercises(userID):
    """
    return (list of exercises from database): a list of exercises that
    the user is tracking
    """
    query = "SELECT DISTINCT * FROM userexercises WHERE userID = %d" % userID
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()["Result"]
    exercises = list(map(lambda x: getExerciseFromID(x[2]), res))
    return exercises


def getUntrackedIDs(categories, numUntracked, trackedIDs):
    """
    return (list of integers): a list of IDs that the user has not selected
    from tracked exercises
    """
    assert numUntracked >= 0
    for category in categories:
        assert category in dbCategories
    query = getExQuery(categories)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
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
def getFitnessTest(categories, numExercises, trackedIDs):
    """
    return (list of exercises from db): exercises to be recommended for
    the fitness test
    """
    assert numExercises > 0
    assert len(trackedIDs) <= numExercises
    for category in categories:
        assert category in dbCategories
    numUntracked = numExercises - len(trackedIDs)    
    untrackedIDs = getUntrackedIDs(categories, numUntracked, trackedIDs)
    exerciseIDs = trackedIDs + untrackedIDs
    assert len(exerciseIDs) == numExercises
    exercises = []
    for ID in exerciseIDs:
        query = "SELECT * FROM exercises WHERE id = %d" % ID
        r = requests.post(dbURL, data = {'query':query, 'key':key})
        assert r.status_code == requests.codes.ok and len(r.json()["Result"]) == 1
        exercises.append(r.json()["Result"][0])
    assert len(exercises) == numExercises
    return exercises

getFitnessTest

## Add route
def getPreviousResults(userID, exID):
    """
    return (list of userexercises from db): the user's previous attempts
    at the given exercise
    """
    query = "SELECT * FROM userexercises WHERE userID = '%s' AND exID = %s" % (userID, exID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok and "Result" in r.json()
    trials = r.json()["Result"]
    return trials


## Add route
def isTracked(userID, exID): 
    """
    return (boolean): whether the exercises is tracked
    """
    exs = getPreviousResults(userID, exID)
    if exs == []:
        return False
    elif exs[0][5] == 1: ##tracked bit
        return True
    return False


def addExercise(userID, exID, timestamp, rate):
    """
    return (boolean): True upon success
    """
    ct = isTracked(userID, exID)
    if ct == True:
        trackBit = 1
    else:
        trackBit = 0
    query = "INSERT INTO userexercises \
     (userID, exID, timestamp, rate, tracked) \
     VALUES (%d,%d,'%s',%f,%d)" % \
     (userID, exID, timestamp, rate, trackBit)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return True


## Add route
def processMotionData(userID, exID, timestamp, rawdata):
    """
    return (float): the rate of the exercise added
    """
    log = Log(rawdata, data=True)
    rate = log.getFrequency()
    addExercise(userID, exID, timestamp, rate)
    return rate


## Add route
def toggleTracked(userID, exID, clear=False):
    """
    return (list): the userID, exID, and tracked bit
    """
    tracked = getTrackedExercises(userID)
    exIDs = list(map(lambda x:x[0], tracked))
    assert exID in exIDs
    if clear:
        trackBit = 0
    else:
        tracked = isTracked(userID, exID)
    trackBit = 1 - tracked
    query = "UPDATE userexercises SET tracked = %d WHERE userID = '%s' AND exID = '%s'" % (trackBit, userID, exID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return [userID, exID, trackBit]

