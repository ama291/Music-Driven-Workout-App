import unittest
import requests
from Scripts.goal import Goal
from Scripts.user import User
from Scripts.theme import Theme
from Scripts.competition import Competition
from Scripts.driver import *
import jsonpickle

"""
For testing driver.py
NOTE: A return value of 0 means success, 1 means database error, and 2 means invalid action.
"""

dbURL = 'http://138.197.49.155:5000/api/database/'

key = 'SoftCon2018'

class TestDriver(unittest.TestCase):

    def test(self):

        # test getUserId
        username = "test-spotify-user"
        uid = getUserId(username)
        self.assertTrue(uid is None)

        # test onboarding
        uid = onboarding(username, 70, 160, 1995)
        self.assertTrue(uid is not None)
        self.assertEqual(uid, getUserId(username))

        # test getUser
        testUser = getUser(uid)
        self.assertEqual(testUser.ID, uid)
        self.assertEqual(testUser.spotifyUsername, username)
        self.assertEqual(testUser.height, 70)
        self.assertEqual(testUser.weight, 160)
        self.assertEqual(testUser.birthyear, 1995)
        self.assertEqual(testUser.goals, [])
        self.assertEqual(testUser.themes, [])
        self.assertEqual(testUser.competitions, [])
        self.assertEqual(testUser.inProgressWorkouts, {})
        self.assertEqual(testUser.savedWorkouts, {})

        # test getWorkout
        themes = None
        categories = ["Cardio", "Stretching"]
        muscleGroups = None
        equipment = ["Body Only"]
        duration = 50
        difficulty = "Intermediate"
        accessToken = "example-access-token"
        workout = getWorkout(uid, themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)
        print(workout)
        wid = (jsonpickle.decode(workout)).ID

        # test startWorkout
        self.assertEqual(startWorkout(uid, workout), 0)
        self.assertEqual(startWorkout(uid, workout), 2) # workout already in progress

        # test pauseWorkout
        self.assertEqual(pauseWorkout(uid, wid, 1), 0)
        self.assertEqual(pauseWorkout(uid, wid, 2), 0) # can pause as many times as you want

        # test quitWorkout
        self.assertEqual(quitWorkout(uid, wid), 0)
        self.assertEqual(quitWorkout(uid, wid), 2) # can't quit a workout that's not in progress
        self.assertEqual(pauseWorkout(uid, wid, 3), 2) # can't pause a workout that's not in progress
        self.assertEqual(saveWorkout(uid, wid), 2) # can't save workout that has already been quit

        # test saveWorkout
        themes = None
        categories = None
        muscleGroups = ["Biceps"]
        equipment = ["Dumbbell"]
        duration = 30
        difficulty = "Beginner"
        workout = getWorkout(uid, themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)
        wid = (jsonpickle.decode(workout)).ID
        self.assertEqual(startWorkout(uid, workout), 0)
        self.assertEqual(saveWorkout(uid, wid), 0)
        self.assertEqual(saveWorkout(uid, wid), 2) # can't re-save a workout

        # test startSavedWorkout
        self.assertEqual(startSavedWorkout(uid, wid), 0)

        # test unsaveWorkout
        self.assertEqual(unsaveWorkout(uid, wid), 0)
        self.assertEqual(unsaveWorkout(uid, wid), 2) # workout already unsaved
        self.assertEqual(startSavedWorkout(uid, wid), 2) # workout no longer saved
        self.assertEqual(quitWorkout(uid, wid), 2) # workout no longer saved

        ##test addGoal
        goal1 = Goal("goal1", "goal1 description", 1, ['cardio'], ['abs'], 5, 5, True)
        self.assertEqual(addGoal(uid,goal1),0) #addGoal should be successful
        self.assertTrue(goal1 in getUser(uid).goals)

        ##test removeGoal
        self.assertEqual(removeGoal(uid,goal1),0) #remove goal should be successful
        self.assertEqual(getUser(uid).goals,[]) #now user should have no goals left
        self.assertEqual(removeGoal(uid,goal1),2) #FAILURE because user has no goals

        ##test goalsSaved
        self.assertEqual(goalsSaved(uid),'[]')

        ##test themesSaved
        self.assertEqual(themesSaved(uid),'[]')

        ##test addTheme
        theme1 = Theme("beyonce theme","beyonce",5)
        self.assertEqual(addTheme(uid,theme1),0) #add theme should be successful
        self.assertTrue(theme1 in getUser(uid).themes) #now new theme is in user's themes

        ##test removeTheme
        self.assertEqual(removeTheme(uid,theme1),0) # success - should be able to remove recently added theme
        self.assertEqual(removeTheme(uid,theme1),2) #FAILURE because user has no themes

        # remove user so can rerun this test script
        query = 'DELETE from users where id = %d' % uid
        r = requests.post(dbURL, data = {'query': query, 'key': key})
        self.assertTrue(r.json()['Status'] == "Success")


if __name__ == '__main__':
    unittest.main()
