import unittest
import requests
from Scripts.goal import Goal
from Scripts.user import User
from Scripts.theme import Theme
from Scripts.competition import Competition
from Scripts.driver import getUser, addGoal, removeGoal, addTheme, removeTheme, addCompetition, removeCompetition

class TestDriver(unittest.TestCase):

    def test(self):
        ##test getUser
        r = requests.post('http://138.197.49.155:8000/api/database/', data = {'query': "UPDATE users SET goals='[]',themes='[]',competition='[]' where id=2", 'key': 'SoftCon2018'})
        print(r.json()) #clear goals,themes,competitions for testUser for consistent testing

        testUser = getUser(2)
        self.assertEqual(testUser.ID,2)
        self.assertEqual(testUser.name,"TestUser1")
        self.assertEqual(testUser.tracked,{})
        self.assertEqual(testUser.untracked,{})
        self.assertEqual(testUser.goals,[])
        self.assertEqual(testUser.themes,[])
        self.assertEqual(testUser.competitions,[])

        ##test updateInProgressWorkouts
        ##test updateAllWorkouts
        ##test getWorkout
        ##test startWorkout
        ##test startSavedWorkout
        ##test quitWorkout
        ##test pauseWorkout
        ##test saveWorkout
        ##test unsaveWorkout

        ##test addGoal
        goal1 = Goal("goal1", "goal1 description", 1, ['cardio'], ['abs'], 5, 5, True)
        self.assertEqual(addGoal(2,goal1),0)
        self.assertTrue(goal1 in getUser(2).goals)

        ##test removeGoal
        self.assertEqual(removeGoal(2,goal1),0)
        self.assertEqual(getUser(2).goals,[]) #SUCCESS - should be able to remove
        self.assertEqual(removeGoal(2,goal1),2) #FAILURE because user has no goals

        ##test addTheme
        theme1 = Theme("beyonce theme","beyonce",5)
        self.assertEqual(addTheme(2,theme1),0)
        self.assertTrue(theme1 in getUser(2).themes)

        ##test removeTheme
        self.assertEqual(removeTheme(2,theme1),0)
        self.assertEqual(removeTheme(2,theme1),2) #FAILURE because user has no themes

        ##test addCompetition
        # competition1 = Competition("Race", "Who'll get 1st", "02-05-18")
        # self.assertEqual(addCompetition(2,competition1),0)
        # self.assertTrue(competition1 in getUser(2).competitions)
        #
        # ##test removeCompetition
        # self.assertEqual(removeCompetition(2,competition1),0)
        # self.assertEqual(removeCompetition(2,competition1),2) #FAILURE because user has no competitions

if __name__ == '__main__':
    unittest.main()
