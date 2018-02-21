import requests

key = "SoftCon2018"
dbCategories = ["Cardio", "Olympic Weightlifting", "Plyometrics", "Powerlifting", "Strength", "Stretching", "Strongman"]

def getColumnNames(dbURL, table):
    query = "PRAGMA table_info(%s)" % table
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    cols = list(map(lambda x:x[1], r.json()["Result"]))
    return cols


def getResponseDict(dbURL, values, table):
    cols = getColumnNames(dbURL, table)
    assert len(cols) == len(values)
    res = dict(zip(cols, values))
    return res


def getResponseDictList(dbURL, valuesList, table): 
    return list(map(lambda x: getResponseDict(dbURL, x, table), valuesList))


def modifyUsersDatabase():
	cols = getColumnNames()
	print(cols)

if __name__ == '__main__':
	modifyUsersDatabase