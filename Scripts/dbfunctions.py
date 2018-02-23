import requests

key = "SoftCon2018"
dbCategories = ["Cardio", "Olympic Weightlifting", "Plyometrics", "Powerlifting", "Strength", "Stretching", "Strongman"]
testDB = "http://138.197.49.155:5000/api/testdb/"
realDB = "http://138.197.49.155:5000/api/database/"

def getColumnInfo(dbURL, table):
    query = "PRAGMA table_info(%s)" % table
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    cols = r.json()["Result"]
    return cols

def getColumnNames(dbURL, table):
    colInfos = getColumnInfo(dbURL, table)
    cols = list(map(lambda x:x[1], colInfos))
    return cols


def getResponseDict(dbURL, values, table):
    cols = getColumnNames(dbURL, table)
    assert len(cols) == len(values)
    res = dict(zip(cols, values))
    return res


def getResponseDictList(dbURL, valuesList, table): 
    return list(map(lambda x: getResponseDict(dbURL, x, table), valuesList))


def modifyTable(dbURL, table, desiredCols):
    print("database URL: %s" % dbURL)
    cols = getColumnInfo(dbURL, table)
    colNames = getColumnNames(dbURL, table)
    for col in cols:
        colName = col[1]
        colType = col[2].upper()
        print("%s col, type: %s" %(colName, colType))
        if colName in desiredCols:
            if colType == desiredCols[colName]:
                print("\talready of the correct type")
                continue
            else:
                print("\tset type to %s" % desiredCols[colName])
        else:
            print("\tremove col %s" % (col))
    for desired in desiredCols:
        if desired not in colNames:
            print("add col %s: %s" % (desired, desiredCols[desired]))
    
def addCol(dbURL, table, colName, colType):
    query = "ALTER TABLE %s ADD %s %s" % (table, colName, colType)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    print(res)
    return True

def removeCol(dbURL, table, colName):
    query = "ALTER TABLE %s DROP %s" % (table, colName)
    print(query)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    print(res)
    return True

def dropTable(dbURL, table):
    query = "DROP TABLE %s" % table
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    print(res)
    return True

def createTable(dbURL, tableName, desiredCols):
    cols = ""
    for col in desiredCols:
        cols += "  %s %s,\n" % (col, desiredCols[col])
    cols = cols[:-2] + "\n"
    query = "CREATE TABLE %s (\n%s);" % (tableName, cols)
    print(query)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    print(r.json())
    assert r.status_code == requests.codes.ok
    res = r.json()["Result"]
    return res

def createUsersTable():
    testDB = "http://138.197.49.155:5000/api/testdb/"
    compCols = {u'id': u'INT PRIMARY KEY',
        u'name': u'VARCHAR(50)'}
    # createTable(testDB, "competitions", compCols)
    desiredCols = {u'id': u'INTEGER PRIMARY KEY', 
        u'spotifyUsername':u'VARCHAR(50)', 
        u'goals':u'VARCHAR(9999)', 
        u'themes':u'VARCHAR(9999)', 
        # u'competitions':u'INTEGER,\nFOREIGN KEY(competitions) REFERENCES competitions(id)', 
        u'inProgressWorkouts':u'VARCHAR(9999)', 
        u'savedWorkouts': u'VARCHAR(9999)',
        u'height':u'INT',
        u'weight':u'INT',
        u'birthyear':u'YEAR'}
    createTable(testDB, "users", desiredCols)
    cInfo = getColumnInfo(testDB, "users")
    for col in cInfo:
        print("%s: %s" % (col[1], col[2]))

def addUser(dbURL, spotifyUsername, height, weight, birthyear, goals, themes, \
 competitions, inProgressWorkouts, savedWorkouts):
    colsString = "(%s, %s, %s, %s, %s, %s, %s, %s)" % ("spotifyUsername", \
        "height", "weight", "birthyear", "goals", "themes", \
        "inProgressWorkouts", "savedWorkouts")
    valueString = "('%s', %d, %d, %d, '%s', '%s', '%s', '%s')" % (spotifyUsername, \
        height, weight, birthyear, goals, themes, inProgressWorkouts,\
        savedWorkouts)
    query = "INSERT INTO users %s VALUES %s;" % (colsString, valueString)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return True

def modifyRow(dbURL, table, colName, newVal, ID):
    query = "UPDATE %s SET %s = '%s' WHERE id = %d" % (table, colName, newVal, ID)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return r.json()

def clearUserExercise(dbURL, userID):
    query = "DELETE FROM userexercises WHERE userID = '%s'" % userID
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return r.json()

def clearUser(dbURL, userID):
    query = "UPDATE users SET goals='[]', themes='[]', inProgressWorkouts='{}', savedWorkouts='{}' WHERE id=%d" % userID
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    return r.json()


def getUserBySpotifyUsername(dbURL, spotifyUsername):
    query = "SELECT * FROM users WHERE spotifyUsername = '%s'" % spotifyUsername
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok 
    assert "Result" in r.json()
    user = r.json()["Result"][0]
    return getResponseDict(dbURL, user, "users")

def getRowIDsFromSpotifyUsernames(dbURL):
    query = "SELECT rowid, spotifyUsername FROM users"
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok 
    print(r.json())
    return r.json()

def removeDuplicates(dbURL, table, uniqueCol):
    query = "DELETE FROM %s WHERE rowid NOT IN (SELECT MIN(rowid) FROM %s GROUP BY %s)" % (table, table, uniqueCol)
    r = requests.post(dbURL, data = {'query':query, 'key':key})
    assert r.status_code == requests.codes.ok
    res = r.json()
    print(res)
    return res


if __name__ == '__main__':
    print(clearUser(realDB, 1))
