import requests

dbURL = "http://138.197.49.155:8000/api/database/"
key = "SoftCon2018"

query = """CREATE TABLE userexercises 
(id INT AUTO_INCREMENT PRIMARY KEY,
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