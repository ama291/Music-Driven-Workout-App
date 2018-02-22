#!/usr/bin/env python3
from Scripts.user import User
from Scripts.dbfunctions import getResponseDict, getResponseDictList, testDB, realDB
import requests
import jsonpickle
import sqlite3

# constant return values
SUCCESS = 0
DB_FAILURE = 1
FAILURE = 2

dbURL = realDB
"""
Collection of functions that help Users interact with the database
"""

def getUser(uid):
    """
    :param uid: user ID
    :return: User instance, None if error or user does not exist
    """
    query = 'SELECT * FROM users where id = %s' % str(uid)
    r = requests.post(dbURL, data = {'query': query, 'key': 'SoftCon2018'})

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
    query = 'UPDATE users SET inProgressWorkouts = %s where id = %s' % (inProgress, str(user.ID))

    r = requests.post(dbURL, data={'query': query, 'key': 'SoftCon2018'})
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
    query = 'UPDATE users SET inProgressWorkouts = %s, savedWorkouts = %s where id = %s' % (inProgress, saved, str(user.ID))

    r = requests.post(dbURL, data={'query': query, 'key': 'SoftCon2018'})
    if r.json()['Status'] == 'Success':
        return SUCCESS
    else:
        return DB_FAILURE


def getWorkout(uid, themes, categories, muscleGroups, equipment, duration, difficulty):
    """
    :param uid: Int
    :param equipment: List[String]
    :param duration: Int
    :param difficulty: String
    :param categories: List[String]
    :param muscleGroups: List[String]
    :param themes: List[Theme]
    :return: json string, empty if error otherwise pickled Workout instance
    """
    user = getUser(uid)

    if user is None:
        return '{}'

    workout = user.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty)
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
        return updateInProgressWorkouts(user)
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
        return updateInProgressWorkouts(user)
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
    query = 'SELECT inProgressWorkouts FROM users where id = %s' % str(uid)
    r = requests.post(dbURL, data={'query': query, 'key': 'SoftCon2018'})
    if r.json()['Status'] != "Success" or len(r.json()['Result']) == 0:
        return '{}'
    else:
        return r.json()['Result'][0][0]


def workoutsSaved(uid):
    """
    :param uid: user ID
    :return: json string of saved workouts
    """
    query = 'SELECT savedWorkouts FROM users where id = %s' % str(uid)
    r = requests.post(dbURL, data={'query': query, 'key': 'SoftCon2018'})
    if r.json()['Status'] != "Success" or len(r.json()['Result']) == 0:
        return '{}'
    else:
        return r.json()['Result'][0][0]


def addGoal(uid, goal):
    """
    :param uid: user ID
    :param goal: goal to add
    :return: 0 - success, 1 - failure to add to goals in db
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    user.addGoal(goal)

    goalString = jsonpickle.encode(user.goals)
    goalString = "\'" + goalString + "\'"
    sql = "UPDATE users SET goals = %s WHERE id = %d" % (goalString, uid)
    r = requests.post(dbURL, data = {'query': sql, 'key': 'SoftCon2018'})
    if r.json()['Status'] == 'Success':

        return SUCCESS
    else:
        return DB_FAILURE

def removeGoal(uid, goal):
    """
    :param uid: user ID
    :param goal: goal to remove
    :return: 0 - success, 1 - failure to remove goals from db, 2 - goal never added (failed on the user's side)
    """
    user = getUser(uid)
    if(user.removeGoal(goal)):
        goalString = "\'" + jsonpickle.encode(user.goals) + "\'"
        sql = "UPDATE users SET goals = %s WHERE id = %s""" % (goalString, uid)
        r = requests.post(dbURL, data = {'query': sql, 'key': 'SoftCon2018'})
        if r.json()['Status'] == 'Success':
    
            return SUCCESS
        else:
            return DB_FAILURE
    else:
        return FAILURE

def addTheme(uid, theme):
    """
    :param uid: user ID
    :param theme: theme to add
    :return: 0 - success, 1 - failure to update users table
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    user.addTheme(theme)
    themeString = "\'" + jsonpickle.encode(user.themes) + "\'"
    sql = "UPDATE users SET themes = %s WHERE id = %s" % (themeString, uid)
    r = requests.post(dbURL, data = {'query': sql, 'key': 'SoftCon2018'})
    if r.json()['Status'] == 'Success':
    
        return SUCCESS
    else:
        return DB_FAILURE

def removeTheme(uid, theme):
    """
    :param uid: user ID
    :param theme: theme to remove
    :return: 0 - success, 1 - failure to update users table, 2 - theme not previously in user's themes
    """
    user = getUser(uid)
    if(user.removeTheme(theme)):
        themeString = "\'" + jsonpickle.encode(user.themes) + "\'"
        sql = "UPDATE users SET themes = %s WHERE id = %s" % (themeString, uid)
        r = requests.post(dbURL, data = {'query': sql, 'key': 'SoftCon2018'})
        if r.json()['Status'] == 'Success':
    
            return SUCCESS
        else:
            return DB_FAILURE
    else:
        return FAILURE

def addCompetition(uid, competition):
    """
    to be used in iteration2
    
    :param uid: user ID
    :param competition: competition to add
    """
    user = getUser(uid)
    if user is None:
        return DB_FAILURE

    user.addCompetition(competition)
    compString = "\'" + jsonpickle.encode(user.competitions) + "\'"
    sql = "UPDATE users SET competition = %s WHERE id = %s" % (compString, uid)
    r = requests.post(dbURL, data = {'query': sql, 'key': 'SoftCon2018'})
    if r.json()['Status'] == 'Success':
   
        return SUCCESS
    else:
        return DB_FAILURE

def removeCompetition(uid, competition):
    """
    to be used in iteration2
    
    :param uid: user ID
    :param competition: competition to remove
    """
    user = getUser(uid)
    if(user.removeCompetition(competition)):
        compString = "\'" + jsonpickle.encode(user.competitions) + "\'"
        sql = "UPDATE users SET competition = %s WHERE id = %s" % (compString, uid)
        r = requests.post(dbURL, data = {'query': sql, 'key': 'SoftCon2018'})
        if r.json()['Status'] == 'Success':

            return SUCCESS
        else:
            return DB_FAILURE
    else:
        return FAILURE

if __name__ == '__main__':
    print(getUser(1))
    workout = getWorkout(1, [], [], [], [], 60, "Beginner")
    # print(startWorkout(1, workout))