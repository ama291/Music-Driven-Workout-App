import requests
import json
import jsonpickle
from sys import argv
from Scripts.dbfunctions import clearUser, realDB
from Scripts.driver import onboarding, getUser
from Scripts.theme import Theme

dbURL = realDB

apiIP = "http://127.0.0.1:5000"
key = "SoftCon2018"

def getURL(rootURL, route):
    return "%s%s" % (rootURL, route)

def makeRequest(route, data):
    url = getURL(apiIP, route)
    r = requests.post(url, data=data)
    print("r.status_code - %s" % r.status_code)
    assert r.status_code == requests.codes.ok
    res = r.json()
    print(res)
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

def getWorkoutExercises(uid, themes, categories, muscleGroups, equipment, duration, difficulty, accessToken):
    route = "/api/workouts/getworkout/"
    data = {"userid": uid, 
        "equipment": equipment, 
        "duration": duration, 
        "difficulty": difficulty, 
        "categories": categories, 
        "musclegroups": muscleGroups, 
        "themes": themes, 
        "token": accessToken,
        "key": key}
    exercises = json.loads(makeRequest(route, data))
    return exercises

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

def getExercisesByType(category, muscleGroup, equipment):
    route = "/api/fitness/getexsbytype/"
    data = {"category": category,
        "muscle": muscleGroup,
        "equipment": equipment,
        "key": key}
    return json.loads(makeRequest(route, data))

def getCategories():
    route = "/api/fitness/getcategories/"
    data = {"key": key}
    return json.loads(makeRequest(route, data))

def getMuscles():
    route = "/api/fitness/getmuscles/"
    data = {"key": key}
    return json.loads(makeRequest(route, data))

def getEquipments():
    route = "/api/fitness/getequipments/"
    data = {"key": key}
    return json.loads(makeRequest(route, data))

def processMotionData(userID, exID, timestamp, rawdata, exact):
    route = "/api/fitness/processmotion/"
    data = {"userid": userID,
        "exid": exID,
        "timestamp": timestamp,
        "rawdata": rawdata,
        "exact": exact,
        "key": key}
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

def removeGoal(uid, name):
    route = "/api/goals/removegoal/"
    data = {"userid": uid,
        "name": name,
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

def removeTheme(uid, themeName):
    route = "/api/themes/removetheme/"
    data = {"userid": uid,
        "themename": themeName,
        "key": key}
    return jsonpickle.decode(makeRequest(route, data))

if __name__ == '__main__':
    if len(argv) != 2:
        pass
    elif argv[1] == "goals":
        print("\nAdd goal")
        print(addGoal(1, "goal1", "goal1 description", 1, ['cardio'], ['abs'], 5, 5, True))
        print(addGoal(1, "goal2", "", 1, ['cardio'], ['abs'], 5, 5, True))
        print(addGoal(1, "goal3", "", 1, ['cardio'], ['abs'], 5, 5, True))
        print(addGoal(1, "goal5", "", 1, ['cardio'], ['abs'], 5, 5, False))

        print("\nRemove goal")
        print(removeGoal(1, "goal1"))
        print(removeGoal(1, "goal2"))
        print(removeGoal(1, "goal2"))

        print("\nAdd Theme")
        print(addTheme(1, "theme1", "Artist", 3))
        print(addTheme(1, "theme3", "Song", 3))

        print("\nRemove Theme")
        print(removeTheme(1, "theme1"))
        print(removeTheme(1, "theme2"))
        clearUser(dbURL, 1)
    elif argv[1] == "workout":
        username = "test-spotify-user"

        # test onboarding
        uid = onboarding(username, 70, 160, 1995)
        # test getUser
        testUser = getUser(uid)
        # test getWorkout
        # get new workout, themes set
        theme1 = Theme("The Killers", "artist", "0C0XlULifJtAgn6ZNCW2eu", 1)
        theme2 = Theme("Otra Vez (feat. J Balvin)", "track", "7pk3EpFtmsOdj8iUhjmeCM", 2)
        theme3 = Theme("Disciples", "track", "2gNfxysfBRfl9Lvi9T3v6R", 3)
        themes = [theme1, theme2, theme3]
        categories = ["Cardio", "Stretching"]
        muscleGroups = None
        equipment = ["Body Only"]
        duration = 50
        difficulty = "Intermediate"
        accessToken = "example-access-token"

        # test get workout exercsies
        exs = getWorkoutExercises(uid, themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)
        for ex in exs:
            print(ex)

        clearUser(dbURL, username)
        # print("\nStart Workout")
        # print(startWorkout(1, workout))
        # print("\nPause Workout")
        # print(pauseWorkout(1, 0))
        # print("\nQuit Workout")
        # print(quitWorkout(1, 0))
        # print("\nSave Workout")
        # print(saveWorkout(1, 0))
        # print("\nUnsave Workout")
        # print(unsaveWorkout(1, 0))
        # print("\nStart Saved Workout")
        # print(startSavedWorkout(1, 0))

        # ## TODO: The following things may not be working
        # # Start saved workout breaks on workouts that haven't been saved
        # # print("\nGet Workouts\n", getWorkout(0, ["Body Only"], 50, "Beginner"))
        # print("\nWorkouts Saved")
        # saved = workoutsSaved(0)
        # print(saved)
        # print(type(saved))

    elif argv[1] == "fitness":
        # print("\nWorkouts In Progress\n", workoutsInProgress(0))
        print("Process motion data")
        with open('Logs/log1.json', 'r') as fd:
                data = fd.read()
        data = processMotionData(1, 12, "2012-12-12 12:12:12", data, False)
        print(data)
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
        print("\nGet Exercises By Type")
        print(getExercisesByType("Strength", "Shoulders", "Body Only"))
        print("\nGet categories")
        print(getCategories())
        print("\nGet muscle groups")
        print(getMuscles())
        print("\nGet equipment")
        print(getEquipments())
