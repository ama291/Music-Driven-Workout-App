#testing example
import unittest
from Scripts.exercise import Exercise
from Scripts.userexercise import UserExercise
from Scripts.user import User

class TestUserExercise(unittest.TestCase):

    def test(self):
        name1 = "Jumping Jacks"
        ex1 = Exercise(name1, 30.0)
        uex1 = UserExercise(ex1, 68.0)
        
        ex2 = Exercise(name1, 30.0)
        uex2 = UserExercise(ex2, 71.0)

        name2 = "High Knees"
        ex3 = Exercise(name2, 30.0)
        uex3 = UserExercise(ex3, 91.0)

        ## test constructor
        usr1 = User("Madeline")
        self.assertEqual(usr1.name, "Madeline")
        # added by Larissa
        self.assertFalse(usr1.workoutsInProgress())
        self.assertFalse(usr1.workoutsSaved())

        ## test trackEx
        usr1.trackEx(uex1)
        self.assertTrue(usr1.exIndexTracked(name1) is not None)
        usr1.trackEx(uex2)
        self.assertEqual(len(usr1.tracked), 1)

        uex2 = UserExercise(ex1, 71.0)
        usr1.trackEx(uex2)
        self.assertTrue(usr1.exIndexTracked(name1) is not None)
        self.assertEqual(len(usr1.tracked), 1)
        self.assertEqual(len(usr1.tracked[0].trials), 3)
        
        ## test untrackEx
        usr1.untrackEx(name1)
        self.assertTrue(usr1.exIndexUntracked(name1) is not None)
        self.assertTrue(usr1.exIndexTracked(name1) is None)

        ## test exIndex
        usr1.trackEx(uex3)
        self.assertEqual(usr1.exIndexTracked(name2), 0)
        usr1.untrackEx(name2)
        self.assertEqual(usr1.exIndexUntracked(name1), 0)
        self.assertEqual(usr1.exIndexUntracked(name2), 1)

        # added by Larissa

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
        # category option
        duration = 50
        difficulty = "Intermediate"
        categories = ["Cardio", "Strength"]
        workout1 = usr1.getWorkout(duration, difficulty, categories=categories)
        w1_ID = workout1.getID()
        self.assertEqual(workout1.getDuration(), duration)
        self.assertEqual(workout1.getDifficulty(), difficulty)
        self.assertEqual(workout1.getCategories(), categories)
        self.assertEqual(workout1.getMuscleGroups(), None)
        self.assertEqual(workout1.getCurrEx(), 0)
        # muscle group option
        duration = 30
        difficulty = "Beginner"
        muscleGroups = ["Chest", "Shoulders", "Biceps"]
        workout2 = usr1.getWorkout(duration, difficulty, muscleGroups=muscleGroups)
        w2_ID = workout2.getID()
        self.assertEqual(workout2.getDuration(), duration)
        self.assertEqual(workout2.getDifficulty(), difficulty)
        self.assertEqual(workout2.getCategories(), None)
        self.assertEqual(workout2.getMuscleGroups(), muscleGroups)
        self.assertEqual(workout2.getCurrEx(), 0)
        # workouts should have unique IDs and not be saved/in progress
        self.assertTrue(w1_ID != w2_ID)
        self.assertFalse(w1_ID in usr1.workoutsInProgress())
        self.assertFalse(w1_ID in usr1.workoutsSaved())
        self.assertFalse(w2_ID in usr1.workoutsInProgress())
        self.assertFalse(w2_ID in usr1.workoutsSaved())

        # test startWorkout
        self.assertTrue(usr1.startWorkout(workout1))
        self.assertTrue(w1_ID in usr1.workoutsInProgress())
        self.assertFalse(w1_ID in usr1.workoutsSaved())
        self.assertTrue(usr1.startWorkout(workout2))
        self.assertTrue(w2_ID in usr1.workoutsInProgress())
        self.assertFalse(w2_ID in usr1.workoutsSaved())
        self.assertFalse(usr1.startWorkout(workout2)) # already in progress

        # test pauseWorkout
        # first pause
        self.assertTrue(usr1.pauseWorkout(w2_ID, 4))
        inProgress = usr1.workoutsInProgress()
        self.assertTrue(w2_ID in inProgress)
        self.assertEqual(inProgress[w2_ID].getCurrEx(), 4)
        # second pause
        self.assertTrue(usr1.pauseWorkout(w2_ID, 7))
        inProgress = usr1.workoutsInProgress()
        self.assertTrue(w2_ID in inProgress)
        self.assertEqual(inProgress[w2_ID].getCurrEx(), 7)
        workout3 = usr1.getWorkout(duration, difficulty, categories=categories)
        w3_ID = workout3.getID()
        self.assertFalse(usr1.pauseWorkout(w3_ID, 2)) # cannot pause, was never started

        # test quitWorkout
        self.assertTrue(usr1.quitWorkout(w1_ID))
        self.assertFalse(usr1.pauseWorkout(w1_ID, 3)) # workout completed, can no longer pause
        self.assertFalse(w1_ID in usr1.workoutsInProgress()) # can only save once completed workout
        self.assertFalse(w1_ID in usr1.workoutsSaved())
        self.assertFalse(usr1.quitWorkout(w3_ID)) # cannot quit, was never started

        # test saveWorkout
        self.assertTrue(usr1.saveWorkout(w2_ID))
        self.assertFalse(w2_ID in usr1.workoutsInProgress())
        saved = usr1.workoutsSaved()
        self.assertTrue(w2_ID in saved)
        self.assertEqual(saved[w2_ID].getCurrEx(), 0) # so restarts at first exercise
        self.assertFalse(usr1.saveWorkout(w1_ID))  # was quit, no longer exists
        self.assertFalse(usr1.saveWorkout(w2_ID)) # cannot resave
        self.assertFalse(usr1.saveWorkout(w3_ID))  # cannot save, was never completed

        # test startSavedWorkout
        self.assertFalse(usr1.startSavedWorkout(w1_ID)) # cannot restart, was never saved
        self.assertTrue(usr1.startSavedWorkout(w2_ID))
        self.assertTrue(w2_ID in usr1.workoutsInProgress())
        inProgress = usr1.workoutsInProgress()
        self.assertEqual(inProgress[w2_ID].getCurrEx(), 0)  # restarted at first exercise
        self.assertTrue(w2_ID in usr1.workoutsSaved())
        self.assertTrue(usr1.quitWorkout(w2_ID))
        self.assertFalse(w2_ID in usr1.workoutsInProgress())
        self.assertTrue(w2_ID in usr1.workoutsSaved()) # quiting a saved workout does not unsave it

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




if __name__ == '__main__':
    unittest.main()
