import requests
import json

apiIP = "http://138.197.49.155:8000"
key = "SoftCon2018"

def getURL(rootURL, route):
    return "%s%s" % (rootURL, route)

def makeRequest(route, data):
    url = getURL(apiIP, route)
    r = requests.post(url, data=data)
    assert r.status_code == requests.codes.ok
    return r.json()["Result"]

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


if __name__ == '__main__':
    print(isTracked(1,12))
    print(isTracked(1,123))
    print(isTracked(1,144))
    print("Is Tracked", isTracked(1,12))
    print(isTracked(1,123), type(isTracked(1,123)))
    cats = ["Strength", "Cardio"]
    print("get ftiness test", getFitnessTest(cats, 4, [12, 144]))
    print("Toggle tracked", toggleTracked(1,12))
    print("Get tracked exercises", getTrackedExercises(1, cats))