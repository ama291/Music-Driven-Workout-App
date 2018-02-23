import unittest
import requests
from Scripts.goal import Goal
from Scripts.user import User
from Scripts.theme import Theme
from Scripts.competition import Competition
from Scripts.driver import getUser, addGoal, removeGoal, goalsSaved, themesSaved, addTheme, removeTheme, addCompetition, removeCompetition

"""
For testing driver.py
"""

dbURL = 'http://138.197.49.155:5000/api/database/'
# dbURL = 'http://138.197.49.155:5000/api/testdb/'

key = 'SoftCon2018'

class TestDriver(unittest.TestCase):

    def test(self):
        ##test getUser
        r = requests.post(dbURL, data = {'query': "UPDATE users SET goals='[]',themes='[]', where id=1", 'key': key})
        #clear goals,themes,competitions for testUser for consistent testing

        testUser = getUser(1)
        self.assertEqual(testUser.ID,1)
        self.assertEqual(testUser.spotifyUsername,"Alex")
        self.assertEqual(testUser.goals,[])
        self.assertEqual(testUser.themes,[])
        #self.assertEqual(testUser.competitions,[]) #confirm that the values are cleared
        # self.assertEqual(testUser.inProgressWorkouts, [])
        # self.assertEqual(testUser.savedWorkouts, [])

        ##test addGoal
        goal1 = Goal("goal1", "goal1 description", 1, ['cardio'], ['abs'], 5, 5, True)
        self.assertEqual(addGoal(1,goal1),0) #addGoal should be successful
        self.assertTrue(goal1 in getUser(1).goals)

        ##test removeGoal
        self.assertEqual(removeGoal(1,goal1),0) #remove goal should be successful
        self.assertEqual(getUser(1).goals,[]) #now user should have no goals left
        self.assertEqual(removeGoal(1,goal1),2) #FAILURE because user has no goals

        ##test goalsSaved
        self.assertEqual(goalsSaved(1),'[]')

        ##test themesSaved
        self.assertEqual(themesSaved(1),'[]')

        ##test addTheme
        theme1 = Theme("beyonce theme","beyonce",5)
        self.assertEqual(addTheme(1,theme1),0) #add theme should be successful
        self.assertTrue(theme1 in getUser(1).themes) #now new theme is in user's themes

        ##test removeTheme
        self.assertEqual(removeTheme(1,theme1),0) # success - should be able to remove recently added theme
        self.assertEqual(removeTheme(1,theme1),2) #FAILURE because user has no themes

        ##test addCompetition
        # To be implemented if extra time
        # print(getUser(1))
        # competition1 = Competition("Race", "Who will get 1st", "02-05-18")
        # self.assertEqual(addCompetition(1,competition1),0)
        # self.assertTrue(competition1 in getUser(1).competitions)
        #
        # ##test removeCompetition
        # self.assertEqual(removeCompetition(1,competition1),0)
        # self.assertEqual(removeCompetition(1,competition1),2) #FAILURE because user has no competitions

if __name__ == '__main__':
    unittest.main()
