#!/usr/bin/env python3
from Scripts.user import User
import requests
import jsonpickle
import sqlite3

# constant return values
SUCCESS = 0
DB_FAILURE = 1
FAILURE = 2

def getUser(uid):
    """
    :param uid: user ID
    :return: User instance, None if error
    """
    query = 'SELECT * FROM users where id = %s' % str(uid)
    r = requests.post('http://138.197.49.155:8000/api/database/', data = {'query': query, 'key': 'SoftCon2018'})

    if r.json()['Status'] != 'Success':
        return None

    dbEntry = r.json()['Result'][0]
    ID = dbEntry[0]
    name = dbEntry[1]
    tracked = jsonpickle.decode(dbEntry[2])
    untracked = jsonpickle.decode(dbEntry[3])
    goals = jsonpickle.decode(dbEntry[4])
    themes = jsonpickle.decode(dbEntry[5])
    competitions = jsonpickle.decode(dbEntry[6])
    inProgressWorkouts = jsonpickle.decode(dbEntry[7])
    savedWorkouts = jsonpickle.decode(dbEntry[8])
    user = User(ID, name, tracked, untracked, goals, themes, competitions, inProgressWorkouts, savedWorkouts)
    return user


def updateInProgressWorkouts(user):
    """
    :param user: User instance
    :return: 0 - success, 1 - failure to update users table
    """
    inProgress = "\'" + jsonpickle.encode(user.inProgressWorkouts) + "\'"
    query = 'UPDATE users SET inProgressWorkouts = %s where id = %s' % (inProgress, str(user.ID))

    r = requests.post('http://138.197.49.155:8000/api/database/', data={'query': query, 'key': 'SoftCon2018'})
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

    r = requests.post('http://138.197.49.155:8000/api/database/', data={'query': query, 'key': 'SoftCon2018'})
    if r.json()['Status'] == 'Success':
        return SUCCESS
    else:
        return DB_FAILURE


# getFitnessTest
# exIndexTracked
# exIndexUntracked
# hasEx
# trackEx
# untrackEx


def getWorkout(uid, equipment, duration, difficulty, categories = None, muscleGroups = None, themes = None):
    """
    :param uid: Int
    :param equipment: List[String]
    :param duration: Int
    :param difficulty: String
    :param categories: List[String]
    :param muscleGroups: List[String]
    :param themes: List[Theme]
    :return: Workout instance, None if error
    """
    user = getUser(uid)

    if user is None:
        return None

    workout = user.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty)
    return workout


def startWorkout(uid, workout):
    """
    :param uid: user ID
    :param workout: Workout instance
    :return: 0 - success, 1 - failure to update users table, 2 - workout already in progress
    """
    user = getUser(uid)
    hasStarted = user.startWorkout(workout)

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
    hasUnsaved = user.unsaveWorkout(wid)

    if hasUnsaved:
        return updateAllWorkouts(user)
    else:
        return FAILURE

def addGoal(uid, goal):
    """
    :param uid: user ID
    :param goal: goal to add
    :return: 0 - success, 1 - failure to add to goals in db
    """
    user = getUser(uid)
    user.addGoal(goal)
    db = sqlite3.connect("/Project/Music-Driven-Workout-App/data.db")
    cursor = db.cursor()
    goalString = jsonpickle.encode(user.goals)
    sql = 'UPDATE users
           SET goals = %s
           WHERE id = %s' % (goalString, uid)
    try:
        cursor.execute(sql)
        db.commit()
        return SUCCESS
    except:
        db.rollback()
        return DB_FAILURE

def removeGoal(uid, goal):
    """
    :param uid: user ID
    :param goal: goal to remove
    """
    user = getUser(uid)
    user.removeGoal(goal)
    db = sqlite3.connect("/Project/Music-Driven-Workout-App/data.db")
    cursor = db.cursor()
    goalString = jsonpickle.encode(user.goals)
    sql = 'UPDATE users
           SET goals = %s
           WHERE id = %s' % (goalString, uid)
    try:
        cursor.execute(sql)
        db.commit()
        return SUCCESS
    except:
        db.rollback()
        return DB_FAILURE

# addTheme
# removeTheme
# addCompetition
# removeCompetition
