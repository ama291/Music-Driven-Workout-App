import unittest
from Scripts.goal import Goal
from Scripts.user import User

class TestGoal(unittest.TestCase):

    def test(self):
        goal1 = Goal("goal1", "Complete 5 workouts", 5, ["arms"], ["bicepts"], 14, 3, True)
        #goal2 = Goal("","",-1,[],[],-1,-1,True) <-- correctly causes ValueError
        #goal3 = Goal(None, None, 5, [],[],None, None, True) <-- correctly causes ValueError

        ## test constructor
        self.assertEqual(goal1.name, "goal1")
        self.assertEqual(goal1.description, "Complete 5 workouts")
        self.assertEqual(goal1.duration, 14)
        self.assertEqual(goal1.daysPerWeek, 3)
        self.assertTrue(goal1.notify)
        self.assertFalse(goal1.completed)
        self.assertEqual(goal1.categories, ["arms"])
        self.assertEqual(goal1.muscleGroups, ["bicepts"])

        ## test getCategories
        self.assertEqual(goal1.getCategories(), ["arms"])

        ## test getMuscleGroups
        self.assertEqual(goal1.getMuscleGroups(), ["bicepts"])

        ## test addCategory
        goal1.addCategory("cardio")
        self.assertTrue("cardio" in goal1.getCategories())

        ## test addMuscleGroup
        goal1.addMuscleGroup("tricepts")
        self.assertTrue("tricepts" in goal1.getMuscleGroups())

        ## test makeProgress
        for i in range(5):
            self.assertFalse(goal1.completed)
            goal1.makeProgress()
            self.assertEqual(goal1.progress, i+1)

        ## test completed
        self.assertTrue(goal1.completed)

        ## test editGoalDescription
        goal1.editGoalDescription("Complete 3 workouts")
        self.assertEqual(goal1.description,"Complete 3 workouts")

if __name__ == '__main__':
    unittest.main()
