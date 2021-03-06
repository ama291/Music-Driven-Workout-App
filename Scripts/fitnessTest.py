import requests
from random import randint
import json
from datetime import datetime
from math import ceil
from Scripts.log import Log
from Scripts.dbfunctions import key, dbCategories, getColumnNames, \
  getResponseDictList, getResponseDict, testDB, realDB

dbURL = realDB

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
    r = requests.post(dbURL, data = {'query': query, 'key': key})
    assert r.status_code == requests.codes.ok
    ex = r.json()["Result"][0]
    return getResponseDict(dbURL, ex, "exercises")

def getExercisesGeneric(userID, query):
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()["Result"]
    ## TODO: set instead of list?
    exercises = list(map(lambda x: getExerciseFromID(x[2]), res))
    unique = []
    for ex in exercises:
        if ex not in unique:
            unique.append(ex)
    return unique

def getUserExercises(userID):
    """
    return (list of exercises from database): a list of exercises that
    the user is tracking
    """
    ## TODO: no need for distinct
    query = "SELECT DISTINCT * FROM userexercises WHERE userID = %d" % userID
    exercises = getExercisesGeneric(userID, query)
    return exercises

## Add route
## TODO!!!: consider muscle groups and equipment
def getTrackedExercises(userID, categories=dbCategories):
    query = "SELECT DISTINCT * FROM userexercises WHERE userID = %d AND tracked = 1" % userID
    exs = getExercisesGeneric(userID, query)
    tracked = list(filter(lambda x: x["type"] in categories, exs))
    return tracked

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
    return getResponseDictList(dbURL, exercises, "exercises")


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
    return getResponseDictList(dbURL, trials, "userexercises")


## Add route
def isTracked(userID, exID):
    """
    return (boolean): whether the exercises is tracked
    """
    exs = getPreviousResults(userID, exID)
    if exs == []:
        return False
    elif exs[0]["tracked"] == 1:
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

## add route
def addExerciseExact(userID, exID, timestamp, rate):
    """
    return (boolean): True upon success
    """
    exact = 1
    query = "INSERT INTO userexercises \
     (userID, exID, timestamp, rate, exact) \
     VALUES (%d,%d,'%s',%f,%d)" % \
     (userID, exID, timestamp, rate, exact)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return True


## Add route
def processMotionData(userID, exID, timestamp, rawdata, exact):
    """
    return (float): the rate of the exercise added
    """
    log = Log(rawdata, data=True)
    rate = log.getFrequency() * 60
    if not exact:
        addExercise(userID, exID, timestamp, rate)
    level, leveledUp = getLevel(userID, 5)
    return {"rate":rate , "level":level, "leveledUp":leveledUp}


## Add route
def toggleTracked(userID, exID, clear=False):
    """
    return (list): the userID, exID, and tracked bit
    """
    exs = getUserExercises(userID)
    exIDs = list(map(lambda x:x["id"], exs))
    assert exID in exIDs
    if clear:
        trackBit = 0
    else:
        tracked = isTracked(userID, exID)
    trackBit = 1 - tracked
    query = "UPDATE userexercises SET tracked = %d WHERE userID = '%s' AND exID = '%s'" % (trackBit, userID, exID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return trackBit

def countUserExercises(userID):
    query = "SELECT count(*) FROM userexercises WHERE userID = %d" % userID
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    count = r.json()["Result"][0][0]
    return count

def getLevel(count, levelGap):
    level = int(ceil(float(count) / levelGap))
    if count % levelGap == 1:
        leveledUp = True
    else:
        leveledUp = False
    return level, leveledUp

def getLevelFromUser(userID, levelGap):
    count = countUserExercises(userID)
    return getLevel(count, levelGap)

def getExactRpm(userID, exID):
    query = "SELECT AVG(rate) FROM userexercises WHERE userID = %d AND exID = %d AND exact = 1" % (userID, exID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    assert "Result" in res
    return res["Result"][0][0]

def getFitnessTestRpm(userID, exID, scale):
    query = "SELECT AVG(rate) FROM userexercises WHERE userID = %d AND exID = %d" % (userID, exID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    assert "Result" in res
    if res["Result"][0][0] != None:
        return scale * res["Result"][0][0]
    return None

def _getAverageRpmHelper(exID, exact):
    if exact:
        rel = "="
    else:
        rel = "!="
    query = "SELECT AVG(rate), COUNT(*) FROM userexercises WHERE exID = %d AND exact %s 1" % (exID, rel)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    assert "Result" in res
    avg = res["Result"][0][0]
    count = res["Result"][0][1]
    return avg, count

def getAverageRpmExact(exID):
    return _getAverageRpmHelper(exID, True)

def getAverageRpmFitnessTest(exID, scale):
    avg, count = _getAverageRpmHelper(exID, False)
    if avg is not None:
        return avg * scale, count
    return None, count

def getAverageRpm(exID, scale):
    avgExact, countExact = getAverageRpmExact(exID)
    avgFT, countFT = getAverageRpmFitnessTest(exID, scale)
    if avgExact is None:
        return avgFT
    if avgFT is None:
        return avgExact
    totalCount = float(countExact + countFT)
    return (avgExact * countExact + avgFT * countFT) / totalCount

def getDefaultRpm(exID):
    query = "SELECT rpm FROM exercises WHERE id = %d" % exID
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    assert "Result" in res
    return res["Result"][0][0]


def getRpmForUser(userID, exID, scale, default=None):
    rpm = getExactRpm(userID, exID)
    if rpm is not None:
        return rpm
    rpm = getFitnessTestRpm(userID, exID, scale)
    if rpm is not None:
        return rpm
    rpm = getAverageRpm(exID, scale)
    if rpm is not None:
        return rpm
    rpm = default if default is not None else getDefaultRpm(exID)
    return rpm
