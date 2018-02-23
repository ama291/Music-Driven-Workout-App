import requests
import json
import jsonpickle
from sys import argv
from Scripts.dbfunctions import clearUser, realDB

dbURL = realDB

apiIP = "http://127.0.0.1:5000"
key = "SoftCon2018"

def getURL(rootURL, route):
    return "%s%s" % (rootURL, route)

def makeRequest(route, data):
    url = getURL(apiIP, route)
    r = requests.post(url, data=data)
    # print("r.status_code - %s", r.status_code)
    # print("requests.codes.ok - %s", requests.codes.ok)
    assert r.status_code == requests.codes.ok
    res = r.json()
    assert "Result" in res
    return res["Result"]

def toBool(string):
    string = string.lower()
    assert string in ["true", "false"]
    if string == "true":
        return True
    return False


def getWorkout(uid, equipment, duration, difficulty, categories=None, muscleGroups=None, themes=None):
    route = "/api/workouts/getworkout/"
    data = {"userid": uid, "equipment": equipment, "duration": duration, "difficulty": difficulty, "categories": categories, "musclegroups": muscleGroups, "themes": themes, "key": key}
    workout = json.loads(jsonpickle.decode(makeRequest(route, data)))
    return workout

def startWorkout(uid, workout):
    route = "/api/workouts/startworkout/"
    data = {"userid": uid, "workout": json.dumps(workout), "key": key}
    return int(makeRequest(route, data))

def pauseWorkout(uid, wid):
    route = "/api/workouts/pauseworkout/"
    data = {"userid": uid, "workoutid": wid, "key": key}
    return int(makeRequest(route, data))

def quitWorkout(uid, wid):
    route = "/api/workouts/quitworkout/"
    data = {"userid": uid, "workoutid": wid, "key": key}
    return int(makeRequest(route, data))

def saveWorkout(uid, wid):
    route = "/api/workouts/saveworkout/"
    data = {"userid": uid, "workoutid": wid, "key": key}
    return int(makeRequest(route, data))

def unsaveWorkout(uid, wid):
    route = "/api/workouts/unsaveworkout/"
    data = {"userid": uid, "workoutid": wid, "key": key}
    return int(makeRequest(route, data))

def startSavedWorkout(uid, wid):
    route = "/api/workouts/startsavedworkout/"
    data = {"userid": uid, "workoutid": wid, "key": key}
    return int(makeRequest(route, data))

def workoutsSaved(uid):
    route = "/api/workouts/workoutssaved/"
    data = {"userid": uid, "key": key}
    return json.loads(jsonpickle.decode(makeRequest(route, data)))

def workoutsInProgress(uid):
    route = "/api/workouts/workoutsinprogress/"
    data = {"userid": uid, "key": key}
    return json.loads(jsonpickle.decode(makeRequest(route, data)))

def isTracked(userID, exID):
    route = "/api/fitness/istracked/"
    data = {"userid": userID, "exid": exID, "key": key}
    return toBool(makeRequest(route, data))

def getTrackedExercises(userID, categories):
    route = "/api/fitness/tracked/"
    data = {"userid": userID, "categories": categories, "key": key}
    return json.loads(makeRequest(route, data))

def getFitnessTest(categories, numExercises, trackedIDs):
    route = "/api/fitness/test/"
    data = {"categories": categories, "numexercises": numExercises, "exerciseids": trackedIDs, "key": key}
    return json.loads(makeRequest(route, data))

def addExerciseExact(userID, exID, timestamp, rate):
    route = "/api/fitness/addexact/"
    data = {"userid": userID,
        "exid": exID,
        "timestamp": timestamp,
        "rate": rate,
        "key": key}
    return toBool(makeRequest(route, data))

def toggleTracked(userID, exID):
    route = "/api/fitness/toggletracked/"
    data = {"userid": userID, "exid": exID, "key": key}
    return json.loads(makeRequest(route, data))

def getExerciseFromID(exID):
    route = "/api/fitness/getexercise/"
    data = {"exid": exID, "key": key}
    return json.loads(makeRequest(route, data))

def getUserExercises(userID):
    route = "/api/fitenss/getuserexercises/"
    data = {"userid": userID, "key": key}
    return json.loads(makeRequest(route, data))

def getPreviousResults(userID, exID):
    route = "/api/fitness/getprevious/"
    data = {"userid": userID, "exid": exID, "key": key}
    return json.loads(makeRequest(route, data))

def addGoal(uid, name, description, goalNum, categories, \
     muscleGroups, duration, daysPerWeek, notify):
    route = "/api/goals/addgoal/"
    data = {"userid": uid,
        "name": name,
        "description": description,
        "goalnum": goalNum,
        "categories": categories,
        "musclegroups": muscleGroups,
        "duration": duration,
        "daysperweek": daysPerWeek,
        "notify": notify,
        "key": key}
    return jsonpickle.decode(makeRequest(route, data))

def removeGoal(uid, name, description, goalNum, categories, \
     muscleGroups, duration, daysPerWeek, notify):
    route = "/api/goals/removegoal/"
    data = {"userid": uid,
        "name": name,
        "description": description,
        "goalnum": goalNum,
        "categories": categories,
        "musclegroups": muscleGroups,
        "duration": duration,
        "daysperweek": daysPerWeek,
        "notify": notify,
        "key": key}
    return jsonpickle.decode(makeRequest(route, data))

def addTheme(uid, themeName, theme, numWorkouts):
    route = "/api/themes/addtheme/"
    data = {"userid": uid,
        "themename": themeName,
        "theme": theme,
        "numworkouts": numWorkouts,
        "key": key}
    return jsonpickle.decode(makeRequest(route, data))

def removeTheme(uid, themeName, theme, numWorkouts):
    route = "/api/themes/removetheme/"
    data = {"userid": uid,
        "themename": themeName,
        "theme": theme,
        "numworkouts": numWorkouts,
        "key": key}
    return jsonpickle.decode(makeRequest(route, data))

if __name__ == '__main__':
    if len(argv) != 2:
        pass
    elif argv[1] == "goals":
        print("\nAdd goal")
        print(addGoal(1, "goal1", "goal1 description", 1, ['cardio'], ['abs'], 5, 5, True))
        print(addGoal(1, "goal2", "", 1, ['cardio'], ['abs'], 5, 5, True))
        print(addGoal(2, "goal3", "", 1, ['cardio'], ['abs'], 5, 5, True))
        # throws assertion error:
        # print(addGoal(1, "goal4", "", 1, [''], [''], None, 0, True))
        # print(addGoal(1, "goal5", "", 1, ['cardio'], ['abs'], 5, 5, None))

        print("\nRemove goal")
        print(removeGoal(1, "goal1", "goal1 description", 1, ['cardio'], ['abs'], 5, 5, True))
        print(removeGoal(1, "goal2", "wrong description", 1, ['cardio'], ['abs'], 5, 5, True))
        print(removeGoal(1, "goal2", "", 1, ['cardio'], ['abs'], 5, 5, True))

        print("\nAdd Theme")
        print(addTheme(1, "theme1", "Artist", 3))
        print(addTheme(2, "theme3", "Song", 3))

        print("\nRemove Theme")
        print(removeTheme(1, "theme1", "Artist", 3))
        print(removeTheme(1, "theme2", "Artist", 3))
        clearUser(dbURL, 1)
        clearUser(dbURL, 2)
    elif argv[1] == "workout":
        workout = getWorkout(1, ["Body Only", "Kettlebells"], 50, "Intermediate", categories=["Cardio","Stretching"])
        print("\nGet Workouts")
        print(workout)
        print("\nStart Workout")
        print(startWorkout(1, workout))
        print("\nPause Workout")
        print(pauseWorkout(1, 0))
        print("\nQuit Workout")
        print(quitWorkout(1, 0))
        print("\nSave Workout")
        print(saveWorkout(1, 0))
        print("\nUnsave Workout")
        print(unsaveWorkout(1, 0))
        print("\nStart Saved Workout")
        print(startSavedWorkout(1, 0))

        ## TODO: The following things may not be working
        # Start saved workout breaks on workouts that haven't been saved
        # print("\nGet Workouts\n", getWorkout(0, ["Body Only"], 50, "Beginner"))
        print("\nWorkouts Saved")
        saved = workoutsSaved(0)
        print(saved)
        print(type(saved))

    elif argv[1] == "fitness":
        # print("\nWorkouts In Progress\n", workoutsInProgress(0))
        print("\nAdd exercise exact")
        time = "2012-12-12 12:12:12"
        print(addExerciseExact(1, 24, time, 25.6))
        print("\nIs Tracked")
        print(isTracked(1,12))
        print("\nIs Tracked")
        print(isTracked(1,123))
        cats = ["Strength", "Cardio"]
        print("\nget ftiness test")
        print(getFitnessTest(cats, 4, [12, 144]))
        print("\nToggle tracked")
        print(toggleTracked(1,12))
        print(toggleTracked(1,12))
        print("\nGet tracked exercises")
        print(getTrackedExercises(1, cats))
        print("\nGet Exercise from ID")
        print(getExerciseFromID(12))
        print("\nGet User Exercises")
        print(getUserExercises(1))
        print("\nGet Previous Results")
        print(getPreviousResults(1,12))