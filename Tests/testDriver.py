import unittest
import requests
from Scripts.goal import Goal
from Scripts.user import User
from Scripts.theme import Theme
from Scripts.competition import Competition
from Scripts.driver import getUser, addGoal, removeGoal, addTheme, removeTheme, addCompetition, removeCompetition

"""
For testing driver.py
"""

class TestDriver(unittest.TestCase):

    def test(self):
        ##test getUser
        r = requests.post('http://138.197.49.155:5000/api/database/', data = {'query': "UPDATE users SET goals='[]',themes='[]',competition='[]' where id=2", 'key': 'SoftCon2018'})
        #print(r.json()) #clear goals,themes,competitions for testUser for consistent testing

        testUser = getUser(2)
        self.assertEqual(testUser.ID,2)
        self.assertEqual(testUser.name,"TestUser1")
        self.assertEqual(testUser.tracked,{})
        self.assertEqual(testUser.untracked,{})
        self.assertEqual(testUser.goals,[])
        self.assertEqual(testUser.themes,[])
        self.assertEqual(testUser.competitions,[]) #confirm that the values are cleared

        ##test addGoal
        goal1 = Goal("goal1", "goal1 description", 1, ['cardio'], ['abs'], 5, 5, True)
        self.assertEqual(addGoal(2,goal1),0) #addGoal should be successful
        self.assertTrue(goal1 in getUser(2).goals)

        ##test removeGoal
        self.assertEqual(removeGoal(2,goal1),0) #remove goal should be successful
        self.assertEqual(getUser(2).goals,[]) #now user should have no goals left
        self.assertEqual(removeGoal(2,goal1),2) #FAILURE because user has no goals

        ##test addTheme
        theme1 = Theme("beyonce theme","beyonce",5)
        self.assertEqual(addTheme(2,theme1),0) #add theme should be successful
        self.assertTrue(theme1 in getUser(2).themes) #now new theme is in user's themes

        ##test removeTheme
        self.assertEqual(removeTheme(2,theme1),0) # success - should be able to remove recently added theme
        self.assertEqual(removeTheme(2,theme1),2) #FAILURE because user has no themes

        ##test addCompetition
        # to be implemented in iteration 2
        # competition1 = Competition("Race", "Who'll get 1st", "02-05-18")
        # self.assertEqual(addCompetition(2,competition1),0)
        # self.assertTrue(competition1 in getUser(2).competitions)
        #
        # ##test removeCompetition
        # self.assertEqual(removeCompetition(2,competition1),0)
        # self.assertEqual(removeCompetition(2,competition1),2) #FAILURE because user has no competitions

if __name__ == '__main__':
    unittest.main()
