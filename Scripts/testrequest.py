#testrequest.py
import requests

# Make request to API
r = requests.post('http://138.197.49.155:5000/api/database/', data = {'query': 'SELECT * FROM users', 'key': 'SoftCon2018'})
print(r.json())

