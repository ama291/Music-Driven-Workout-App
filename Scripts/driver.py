#!/usr/bin/env python3
from Scripts.user import User
from Scripts.goal import Goal
from Scripts.theme import Theme
import random
from Scripts.dbfunctions import getResponseDict, getResponseDictList, testDB, realDB, addUser, getAllFromColumn
import requests
import jsonpickle
import sqlite3

# constant return values
SUCCESS = 0
DB_FAILURE = 1
FAILURE = 2

dbURL = realDB
key = "SoftCon2018"
"""
Collection of functions that help Users interact with the database
"""

def getUserId(username):
    """
    :param username: spotify user ID
    :return: row id in users table - None if first time logging in
    """

    name = "\'" + username + "\'"
    query = 'SELECT id FROM users where spotifyUsername = %s' % name
    r = requests.post(dbURL, data={'query': query, 'key': key})
    if len(r.json()['Result']) != 0:
        return r.json()['Result'][0][0]
    else:
        return None

def onboarding(username, height, weight, year):
    """
    :param username: spotify user ID
    :param height: user height
    :param weight: user weight
    :param year: user birthyear
    :return: assigned row id in users table
    """
    frozenDict = "\'" + jsonpickle.encode({}) + "\'"
    frozenList = "\'" + jsonpickle.encode([]) + "\'"
    name = "\'" + username + "\'"
    query = 'insert into users (spotifyUsername, height, \
            weight, birthyear, goals, themes, \
            inProgressWorkouts, savedWorkouts) values \
                (%s, %d, %d, %d, %s, %s, %s, %s)' \
            % (name, height, weight, year,
            frozenList, frozenList, frozenDict, frozenDict)
    r = requests.post(dbURL, data = {'query': query, 'key': key})
    # now get assigned user id
    query = 'SELECT id FROM users where spotifyUsername = %s' % name
    r = requests.post(dbURL, data={'query': query, 'key': key})
    return r.json()['Result'][0][0]


def getUser(uid):
    """
    :param uid: user ID
    :return: User instance, None if error or user does not exist
    """
    query = 'SELECT * FROM users where id = %d' % uid
    r = requests.post(dbURL, data = {'query': query, 'key': key})

    if r.json()['Status'] != 'Success' or len(r.json()['Result']) == 0:
        return None

    dbEntry = r.json()['Result'][0]
    res = getResponseDict(dbURL, dbEntry, "users")
    ID = res['id']
    spotifyUsername = res['spotifyUsername']
    height = res['height']
    weight = res['weight']
    birthyear = res['birthyear']
    goals = jsonpickle.decode(res['goals'])
    themes = jsonpickle.decode(res['themes'])
    competitions = []
    inProgressWorkouts = jsonpickle.decode(res['inProgressWorkouts'])
    savedWorkouts = jsonpickle.decode(res['savedWorkouts'])
    user = User(ID, spotifyUsername, height, weight, birthyear, goals, themes, competitions, inProgressWorkouts, savedWorkouts)

    return user


def updateInProgressWorkouts(user):
    """
    :param user: User instance
    :return: 0 - success, 1 - failure to update users table
    """
    inProgress = "\'" + jsonpickle.encode(user.inProgressWorkouts) + "\'"
    query = 'UPDATE users SET inProgressWorkouts = %s where id = %d' % (inProgress, user.ID)

    r = requests.post(dbURL, data={'query': query, 'key': key})
    if r.json()['Status'] == 'Success':
        return SUCCESS
    else:
        return DB_FAILURE


def updateAllWorkouts(user):
    """
    :param user: User instance
    :return: 0 - success, 1 - failure to update users table
    """
    inProgress = "\'" + jsonpickle.encode(user.inProgressWorkouts) + "\'"
    saved = "\'" + jsonpickle.encode(user.savedWorkouts) + "\'"
    query = 'UPDATE users SET inProgressWorkouts = %s, savedWorkouts = %s where id = %d' % (inProgress, saved, user.ID)

    r = requests.post(dbURL, data={'query': query, 'key': key})
    if r.json()['Status'] == 'Success':
        return SUCCESS
    else:
        return DB_FAILURE

def updateInProgressAndGoals(user):
    """
    :param user: User instance
    :return: 0 - success, 1 - failure to update users table
    """
    inProgress = "\'" + jsonpickle.encode(user.inProgressWorkouts) + "\'"
    goals = "\'" + jsonpickle.encode(user.goals) + "\'"
    query = 'UPDATE users SET inProgressWorkouts = %s, goals = %s where id = %d' % (inProgress, goals, user.ID)

    r = requests.post(dbURL, data={'query': query, 'key': key})
    if r.json()['Status'] == 'Success':
        return SUCCESS
    else:
        return DB_FAILURE


def getWorkout(uid, themes, categories, muscleGroups, equipment, duration, difficulty, accessToken):
    """
    :param uid: Int
    :param equipment: List[String]
    :param duration: Int
    :param difficulty: String
    :param categories: List[String]
    :param muscleGroups: List[String]
    :param themes: List[Theme]
    :param accessToken: String
    :return: json string, empty if error otherwise pickled Workout instance
    """
    user = getUser(uid)

    if user is None:
        return '{}'

    workout = user.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)
    return '{}' if workout is None else jsonpickle.encode(workout)


def startWorkout(uid, workout):
    """
    :param uid: user ID
    :param workout: json string
    :return: 0 - success, 1 - failure to update users table, 2 - workout already in progress
    """
    if workout == '{}':
        return FAILURE

    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    decoded = jsonpickle.decode(workout)
    hasStarted = user.startWorkout(decoded)

    if hasStarted:
        return updateInProgressAndGoals(user)
    else:
        return FAILURE



def startSavedWorkout(uid, wid):
    """
    :param uid: user ID
    :param wid: workout ID
    :return: 0 - success, 1 - failure to update users table, 2 - workout not saved or already in progress
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    hasStarted = user.startSavedWorkout(wid)

    if hasStarted:
        return updateInProgressAndGoals(user)
    else:
        return FAILURE


def quitWorkout(uid, wid):
    """
    :param uid: user ID
    :param wid: workout ID
    :return: 0 - success, 1 - failure to update users table, 2 - workout was not in progress
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    hasQuit = user.quitWorkout(wid)

    if hasQuit:
        return updateInProgressWorkouts(user)
    else:
        return FAILURE

def pauseWorkout(uid, wid, pausedOn):
    """
    :param uid:  user ID
    :param wid: workout ID
    :param pausedOn: exercise to pause on
    :return: 0 - success, 1 - failure to update users table, 2 - workout not in progress
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    hasPaused = user.pauseWorkout(wid, pausedOn)

    if hasPaused:
        return updateInProgressWorkouts(user)
    else:
        return FAILURE


def saveWorkout(uid, wid):
    """
    :param uid: user ID
    :param wid: workout ID
    :return: 0 - success, 1 - failure to update users table, 2 - workout not in progress or already saved
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    hasSaved = user.saveWorkout(wid)

    if hasSaved:
        return updateAllWorkouts(user)
    else:
        return FAILURE


def unsaveWorkout(uid, wid):
    """
    :param uid: user ID
    :param wid: workout ID
    :return: 0 - success, 1 - failure to update users table, 2 - workout not previously saved
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    hasUnsaved = user.unsaveWorkout(wid)

    if hasUnsaved:
        return updateAllWorkouts(user)
    else:
        return FAILURE


def workoutsInProgress(uid):
    """
    :param uid: user ID
    :return: json string of in progress workouts
    """
    query = 'SELECT inProgressWorkouts FROM users where id = %d' % uid
    r = requests.post(dbURL, data={'query': query, 'key': key})
    if r.json()['Status'] != "Success" or len(r.json()['Result']) == 0:
        return '{}'
    else:
        return r.json()['Result'][0][0]


def workoutsSaved(uid):
    """
    :param uid: user ID
    :return: json string of saved workouts
    """
    query = 'SELECT savedWorkouts FROM users where id = %d' % uid
    r = requests.post(dbURL, data={'query': query, 'key': key})
    if r.json()['Status'] != "Success" or len(r.json()['Result']) == 0:
        return '{}'
    else:
        return r.json()['Result'][0][0]

def addGoal(uid, name, description, goalNum, categories, muscleGroups,\
     duration, daysPerWeek, notify):

    """
    :param uid: user ID
    :param goal: goal to add
    :return: 0 - success, 1 - failure to add to goals in db
    """
    goal = Goal(name, description, goalNum, categories, \
        muscleGroups, duration, daysPerWeek, notify)
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    user.addGoal(goal)

    goalString = jsonpickle.encode(user.goals)
    goalString = "\'" + goalString + "\'"
    sql = "UPDATE users SET goals = %s WHERE id = %d" % (goalString, uid)
    r = requests.post(dbURL, data = {'query': sql, 'key': key})
    if r.json()['Status'] == 'Success':
        return SUCCESS
    else:
        return DB_FAILURE

def removeGoal(uid, name):
    """
    :param uid: user ID
    :param goal: goal to remove
    :return: 0 - success, 1 - failure to remove goals from db, 2 - goal never added (failed on the user's side)
    """
    user = getUser(uid)
    if(user.removeGoal(name)):
        goalString = "\'" + jsonpickle.encode(user.goals) + "\'"
        sql = "UPDATE users SET goals = %s WHERE id = %d" % (goalString, uid)
        r = requests.post(dbURL, data = {'query': sql, 'key': key})
        if r.json()['Status'] == 'Success':
            return SUCCESS
        else:
            return DB_FAILURE
    else:
        return FAILURE

def goalsSaved(uid):
    """
    :param uid: user ID
    :return: json string of saved goals
    """
    query = 'SELECT goals FROM users where id = %d' % uid
    r = requests.post(dbURL, data={'query': query, 'key': key})
    if r.json()['Status'] != "Success" or len(r.json()['Result']) == 0:
        return '{}'
    else:
        return r.json()['Result'][0][0]

def themesSaved(uid):
    """
    :param uid: user ID
    :return: json string of saved themes
    """
    query = 'SELECT themes FROM users where id = %d' % uid
    r = requests.post(dbURL, data={'query': query, 'key': key})
    if r.json()['Status'] != "Success" or len(r.json()['Result']) == 0:
        return '{}'
    else:
        return r.json()['Result'][0][0]

def addTheme(uid, themeName, theme, spotifyId, numWorkouts):
    """
    :param uid: user ID
    :param theme: theme to add
    :return: 0 - success, 1 - failure to update users table
    """
    fullTheme = Theme(themeName, theme, spotifyId, numWorkouts)
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    user.addTheme(fullTheme)
    themeString = "\'" + jsonpickle.encode(user.themes) + "\'"
    sql = "UPDATE users SET themes = %s WHERE id = %d" % (themeString, uid)
    r = requests.post(dbURL, data = {'query': sql, 'key': key})
    if r.json()['Status'] == 'Success':

        return SUCCESS
    else:
        return DB_FAILURE

def removeTheme(uid, themeName):
    """
    :param uid: user ID
    :param theme: theme to remove
    :return: 0 - success, 1 - failure to update users table, 2 - theme not previously in user's themes
    """
    user = getUser(uid)
    if(user.removeTheme(themeName)):
        themeString = "\'" + jsonpickle.encode(user.themes) + "\'"
        sql = "UPDATE users SET themes = %s WHERE id = %d" % (themeString, uid)
        r = requests.post(dbURL, data = {'query': sql, 'key': key})
        if r.json()['Status'] == 'Success':
            return SUCCESS
        else:
            return DB_FAILURE
    else:
        return FAILURE

def addCompetition(uid, competition):
    """
    :param uid: user ID
    :param competition: competition to add
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    user.addCompetition(competition)
    compString = "\'" + jsonpickle.encode(user.competitions) + "\'"
    sql = "UPDATE users SET competitions = %s WHERE id = %d" % (compString, uid)
    r = requests.post(dbURL, data = {'query': sql, 'key': key})
    if r.json()['Status'] == 'Success':
        return SUCCESS
    else:
        return DB_FAILURE

def removeCompetition(uid, competition):
    """
    :param uid: user ID
    :param competition: competition to remove
    """
    user = getUser(uid)
    if(user.removeCompetition(competition)):
        compString = "\'" + jsonpickle.encode(user.competitions) + "\'"
        sql = "UPDATE users SET competitions = %s WHERE id = %d" % (compString, uid)
        r = requests.post(dbURL, data = {'query': sql, 'key': key})
        if r.json()['Status'] == 'Success':
            return SUCCESS
        else:
            return DB_FAILURE
    else:
        return FAILURE

def getInStr(column, lst):
    string = ""
    for i in lst:
        string += "'%s'," % i 
    return "%s IN (%s)" % (column, string[:-1])

def getExercisesReqStr(category, muscleGroup, equipment):
    allCats = getAllFromColumn(dbURL, "exercises", "type")
    allMuscles = getAllFromColumn(dbURL, "exercises", "muscle")
    allEquips = getAllFromColumn(dbURL, "exercises", "equipment")
    if category == "Any":
        catStr = getInStr("type", allCats)
    else:
        assert category in allCats
        catStr = "type = '%s'" % category
    if muscleGroup == "Any":
        muscStr = getInStr("muscle", allMuscles)
    else:
        assert muscleGroup in allMuscles
        muscStr = "muscle = '%s'" % muscleGroup
    if equipment == "Any":
        equipStr = getInStr("equipment", allEquips)
    else: 
        assert equipment in allEquips
        equipStr = "equipment = '%s'" % equipment
    query = "SELECT * FROM exercises WHERE %s AND %s AND %s" % (catStr, \
        muscStr, equipStr)
    return query

def getExercisesbyType(category, muscleGroup, equipment):
    query = getExercisesReqStr(category, muscleGroup, equipment)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    assert "Result" in res
    d = getResponseDictList(dbURL, res["Result"], "exercises")
    return d 

if __name__ == '__main__':
    res = getExercisesReqStr("Strength", "Any", "Body Only")
    print(res)