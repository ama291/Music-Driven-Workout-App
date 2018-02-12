#testrequest.py
import requests

#make request to API
r = requests.post('http://138.197.49.155:8000/api/database/', data = {'query': 'select * from users', 'key': 'SoftCon2018'})
print(r.json())