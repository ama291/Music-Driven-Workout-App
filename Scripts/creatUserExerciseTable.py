import requests

dbURL = "http://138.197.49.155:5000/api/database/"
key = "SoftCon2018"

def deleteOldTable():
	query = "DROP TABLE userexercises"

	data = {"query": query, "key": key}

	r = requests.post(dbURL, data)

	print(r.json())

def makeTable():
	query = """CREATE TABLE userexercises 
	(id INTEGER NOT NULL PRIMARY KEY,
	userID INT,
	exID INT,
	timestamp TIMESTAMP, 
	rate DOUBLE,
	tracked BIT
	);
	"""

	data = {"query": query, "key": key}

	r = requests.post(dbURL, data)

	print(r.json())

if __name__ == '__main__':
	deleteOldTable()
	makeTable()