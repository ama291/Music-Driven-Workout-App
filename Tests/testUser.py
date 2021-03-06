import unittest
from Scripts.exercise import Exercise
from Scripts.user import User
from Scripts.goal import Goal
from Scripts.theme import Theme
from Scripts.competition import Competition
from datetime import datetime


class TestUser(unittest.TestCase):

    def test(self):
        ## test constructor (ID, name tracked,
        ## untracked, goals, themes, competition,
        ## inProgressWorkouts, savedWorkouts)
        usr1 = User(0, "Alex", 167, 150, 1996, [], [], [], {}, {})
        self.assertEqual(usr1.spotifyUsername, "Alex")
        self.assertEqual(usr1.ID, 0)
        self.assertEqual(usr1.height, 167)
        self.assertEqual(usr1.weight, 150)
        self.assertEqual(usr1.birthyear, 1996)
        self.assertEqual(usr1.goals, [])
        self.assertEqual(usr1.themes, [])
        self.assertEqual(usr1.inProgressWorkouts, {})
        self.assertEqual(usr1.savedWorkouts, {})
        self.assertEqual(usr1.level, 0)

        """
        Workout flow - User keeps getting workouts until they find one they like,
        then they start the workout. They can pause multiple times during a workout,
        and resuming the workout should bring them to the exercise that was paused
        on. The user can also choose to quit rather than resume. Once a new workout
        is complete, the user can either quit or save the workout. A new workout can
        only be saved once it has been completed. The user can start a saved workout,
        but there can only one version of this saved workout in progress at a time.
        Once the saved workout is completed, the user can quit or unsave the workout.
        The user can also separately unsave the workout, and this also removes any in
        progress version of the workout. Visiting the proper page loads in all in
        progress and saved workouts for the user to see, from here they can choose
        to start/resume one of these workouts.
        """

        # test getWorkout
        accessToken = "example-access-token"
        # category option
        themes = None
        categories = ["Cardio", "Stretching"]
        muscleGroups = None
        equipment = ["Body Only"]
        duration = 50
        difficulty = "Intermediate"
        workout1 = usr1.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)
        self.assertTrue(workout1 is not None) # None in case of request failure
        w1_ID = workout1.ID
        # muscle group option
        themes = None
        categories = None
        muscleGroups = ["Chest", "Shoulders", "Biceps"]
        equipment = ["Kettlebells", "Machine"]
        duration = 30
        difficulty = "Beginner"
        workout2 = usr1.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)
        self.assertTrue(workout2 is not None)  # None in case of request failure
        w2_ID = workout2.ID

        # workouts should have unique IDs and not be saved/in progress
        self.assertTrue(w1_ID != w2_ID)
        self.assertFalse(w1_ID in usr1.workoutsInProgress())
        self.assertFalse(w1_ID in usr1.workoutsSaved())
        self.assertFalse(w2_ID in usr1.workoutsInProgress())
        self.assertFalse(w2_ID in usr1.workoutsSaved())

        # test startWorkout
        # also test making progress in a workout based on category/muscle group
        goal0 = Goal("goal0", "Complete a cardio and upper body workout", 2, \
                     ["Cardio"], ["Biceps", "Shoulders"], 14, 3, True)
        usr1.addGoal(goal0)
        self.assertTrue(goal0 in usr1.goals)
        self.assertTrue(usr1.startWorkout(workout1)) # cardio category
        self.assertTrue(goal0 in usr1.goals) # goal not yet completed
        self.assertTrue(w1_ID in usr1.workoutsInProgress())
        self.assertFalse(w1_ID in usr1.workoutsSaved())
        self.assertTrue(usr1.startWorkout(workout2)) # shoulders and biceps muscle groups
        self.assertFalse(goal0 in usr1.goals)  # goal now completed
        self.assertTrue(w2_ID in usr1.workoutsInProgress())
        self.assertFalse(w2_ID in usr1.workoutsSaved())
        self.assertFalse(usr1.startWorkout(workout2)) # already in progress

        # test pauseWorkout
        # first pause
        self.assertTrue(usr1.pauseWorkout(w2_ID, 4))
        inProgress = usr1.workoutsInProgress()
        self.assertTrue(w2_ID in inProgress)
        self.assertEqual(inProgress[w2_ID].currExercise, 4)
        # second pause
        self.assertTrue(usr1.pauseWorkout(w2_ID, 7))
        inProgress = usr1.workoutsInProgress()
        self.assertTrue(w2_ID in inProgress)
        self.assertEqual(inProgress[w2_ID].currExercise, 7)
        # attempt to pause unstarted workout
        themes = None
        categories = ["Strongman", "Strength"]
        muscleGroups = None
        equipment = ["Dumbbell", "Cable"]
        duration = 40
        difficulty = "Beginner"
        workout3 = usr1.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)
        self.assertTrue(workout3 is not None)  # None in case of request failure
        w3_ID = workout3.ID
        self.assertFalse(usr1.pauseWorkout(w3_ID, 2))

        # test quitWorkout
        self.assertTrue(usr1.quitWorkout(w1_ID))
        self.assertFalse(usr1.pauseWorkout(w1_ID, 3)) # workout completed, can no longer pause
        self.assertFalse(w1_ID in usr1.workoutsInProgress())
        self.assertFalse(w1_ID in usr1.workoutsSaved())
        self.assertFalse(usr1.quitWorkout(w3_ID)) # cannot quit, was never started

        # test saveWorkout
        self.assertTrue(usr1.saveWorkout(w2_ID))
        self.assertFalse(w2_ID in usr1.workoutsInProgress()) # can only save if workout has been completed
        saved = usr1.workoutsSaved()
        self.assertTrue(w2_ID in saved)
        self.assertEqual(saved[w2_ID].currExercise, 0) # so restarts at first exercise
        self.assertFalse(usr1.saveWorkout(w1_ID))  # was quit, no longer exists
        self.assertFalse(usr1.saveWorkout(w2_ID)) # cannot resave
        self.assertFalse(usr1.saveWorkout(w3_ID))  # cannot save, was never started

        # test startSavedWorkout
        self.assertFalse(usr1.startSavedWorkout(w1_ID)) # cannot restart, was never saved
        self.assertTrue(usr1.startSavedWorkout(w2_ID))
        inProgress = usr1.workoutsInProgress()
        self.assertTrue(w2_ID in inProgress)
        self.assertEqual(inProgress[w2_ID].currExercise, 0)  # restarted at first exercise
        self.assertTrue(w2_ID in usr1.workoutsSaved())
        self.assertFalse(usr1.startSavedWorkout(w2_ID))  # cannot restart until in progress version is complete
        self.assertTrue(usr1.quitWorkout(w2_ID))
        self.assertFalse(w2_ID in usr1.workoutsInProgress())
        self.assertTrue(w2_ID in usr1.workoutsSaved()) # quiting a saved workout does not unsave it
        self.assertTrue(usr1.startSavedWorkout(w2_ID)) # can now restart
        self.assertTrue(usr1.quitWorkout(w2_ID))

        # test unsaveWorkout
        self.assertTrue(usr1.unsaveWorkout(w2_ID))
        self.assertFalse(w2_ID in usr1.workoutsInProgress())
        self.assertFalse(w2_ID in usr1.workoutsSaved())
        self.assertFalse(usr1.unsaveWorkout(w1_ID)) # cannot unsave, was never saved
        self.assertFalse(usr1.unsaveWorkout(w3_ID))  # cannot unsave, was never saved
        self.assertTrue(usr1.startWorkout(workout3))
        self.assertTrue(usr1.saveWorkout(w3_ID))
        self.assertTrue(usr1.startSavedWorkout(w3_ID))
        self.assertTrue(usr1.unsaveWorkout(w3_ID)) # unsaves and removes in progress version
        self.assertFalse(w3_ID in usr1.workoutsInProgress())
        self.assertFalse(w3_ID in usr1.workoutsSaved())

        # test add goal
        goal1 = Goal("goal1", "Complete 5 workouts", 5,\
         ["arms"], ["bicepts"], 14, 3, True)
        usr1.addGoal(goal1)
        self.assertTrue(goal1 in usr1.goals)

        # test remove goal
        self.assertTrue(usr1.removeGoal(goal1.name))
        self.assertFalse(goal1 in usr1.goals)
        goal2 = Goal("goal2", "Complete 5 workouts", 5,\
         ["arms"], ["bicepts"], 14, 3, True)
        usr1.addGoal(goal1)
        self.assertFalse(usr1.removeGoal(goal2.name))

        # test add theme
        theme1 = Theme("Beyonce theme", "artist", "88", 5)
        self.assertTrue(usr1.addTheme(theme1))
        self.assertTrue(theme1 in usr1.themes)
        theme2 = Theme("Beyonce theme", "artist", "88", 5)
        self.assertFalse(usr1.addTheme(theme2))

        # test remove theme
        theme2 = Theme("Taylor Swift theme", "artist", "99", 5)
        self.assertFalse(usr1.removeTheme(theme2.name))
        self.assertTrue(usr1.removeTheme(theme1.name))
        self.assertFalse(theme1 in usr1.themes)

        # test add competition
        competition1 = Competition("Race", "Who'll get 1st", "02-05-18")
        usr1.addCompetition(competition1)
        self.assertTrue(competition1 in usr1.competitions)

        # test remove competition
        competition2 = Competition("Contest", "Who'll get 1st", "02-05-18")
        self.assertFalse(usr1.removeCompetition(competition2))
        self.assertTrue(usr1.removeCompetition(competition1))
        self.assertFalse(competition1 in usr1.competitions)



if __name__ == '__main__':
    unittest.main()
