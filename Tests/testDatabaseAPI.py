#testing example
import unittest
import requests
import json

db = 'http://138.197.49.155:5000/api/database/'

class testDatabaseAPI(unittest.TestCase):

    def test(self):
        # Test Access with keys
        r = requests.post(db, data = {'query': 'SELECT * FROM users'})
        self.assertEqual("Failure - Invalid parameters", r.json()["Status"])
        r = requests.post(db, data = {'query': 'SELECT * FROM users', 'key': 'Incorrect Key'})
        self.assertEqual("Failure - Invalid authentication", r.json()["Status"])
        r = requests.post(db, data = {'query': 'SELECT * FROM users', 'key': 'SoftCon2018'})
        self.assertEqual("Success", r.json()["Status"])

        # Test Queries
        r = requests.post(db, data = {'query': 'SELECT *', 'key': 'SoftCon2018'})
        self.assertEqual("Failure - no tables specified", r.json()["Status"])
        r = requests.post(db, data = {'query': 'SELECT', 'key': 'SoftCon2018'})
        self.assertEqual("Failure - near \"SELECT\": syntax error", r.json()["Status"])
        r = requests.post(db, data = {'key': 'SoftCon2018'})
        self.assertEqual("Failure - Invalid parameters", r.json()["Status"])
        r = requests.post(db, data = {'query': '', 'key': 'SoftCon2018'})
        self.assertEqual("Success", r.json()["Status"])

if __name__ == '__main__':
    unittest.main()
