import requests
import json
import jsonpickle

# apiIP = "http://138.197.49.155:8000"
apiIP = "http://127.0.0.1:5000"
key = "SoftCon2018"

def getURL(rootURL, route):
    return "%s%s" % (rootURL, route)

def makeRequest(route, data):
    url = getURL(apiIP, route)
    r = requests.post(url, data=data)
    assert r.status_code == requests.codes.ok
    res = r.json()
    assert "Result" in res
    return res["Result"]

def getWorkout(uid, equipment, duration, difficulty, categories=None, muscleGroups=None, themes=None):
    route = "/api/workouts/getworkout/"
    data = {"userid": uid, "equipment": equipment, "duration": duration, "difficulty": difficulty, "categories": categories, "musclegroups": muscleGroups, "themes": themes, "key": key}
    return jsonpickle.decode(makeRequest(route, data))

def startWorkout(uid, workout):
    route = "/api/workouts/startworkout/"
    data = {"userid": uid, "workout": workout, "key": key}
    return int(makeRequest(route, data))

def pauseWorkout(uid, wid, pausedOn):
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
    return jsonpickle.decode(makeRequest(route, data))

def workoutsInProgress(uid):
    route = "/api/workouts/workoutsinprogress/"
    data = {"userid": uid, "key": key}
    return jsonpickle.decode(makeRequest(route, data))

def isTracked(userID, exID):
    route = "/api/fitness/istracked/"
    data = {"userid": userID, "exid": exID, "key": key}
    return bool(makeRequest(route, data))
    
def getTrackedExercises(userID, categories):
    route = "/api/fitness/tracked/"
    data = {"userid": userID, "categories": categories, "key": key}
    return json.loads(makeRequest(route, data))

def getFitnessTest(categories, numExercises, trackedIDs):
    route = "/api/fitness/test/"
    data = {"categories": categories, "numexercises": numExercises, "exerciseids": trackedIDs, "key": key}
    return json.loads(makeRequest(route, data))

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


if __name__ == '__main__':
    workout = getWorkout(0, ["Body Only", "Kettlebells"], 50, "Intermediate", categories=["Cardio","Stretching"])
    print("\nGet Workouts\n", workout)
    print("\nStart Workout\n", startWorkout(0, workout))
    print("\nPause Workout\n", pauseWorkout(0, 0, False))
    print("\nQuit Workout\n", quitWorkout(0, 0))
    print("\nSave Workout\n", saveWorkout(0, 0))
    print("\nUnsave Workout\n", unsaveWorkout(0, 0))
    print("\nStart Saved Workout\n", startSavedWorkout(0, 0))

    ## TODO: The following things may not be working
    # Start saved workout breaks on workouts that haven't been saved
    # print("\nGet Workouts\n", getWorkout(0, ["Body Only"], 50, "Beginner"))
    # print("\nWorkouts Saved\n", workoutsSaved(0))
    # print("\nWorkouts In Progress\n", workoutsInProgress(0))

    print("\nIs Tracked\n", isTracked(1,12))
    cats = ["Strength", "Cardio"]
    print("\nget ftiness test\n", getFitnessTest(cats, 4, [12, 144]))
    print("\nToggle tracked\n", toggleTracked(1,12))
    print("\nGet tracked exercises\n", getTrackedExercises(1, cats))
    print("\nGet Exercise from ID\n", getExerciseFromID(12))
    print("\nGet User Exercises", getUserExercises(1))
    print("\nGet Previous Results\n", getPreviousResults(1,12))