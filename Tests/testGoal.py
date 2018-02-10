import unittest
from Scripts.goal import Goal
from Scripts.user import User

class TestGoal(unittest.TestCase):

    def test(self):
        goal1 = Goal("goal1", "Complete 5 workouts", 5, 14, 3, True)

        ## test constructor
        self.assertEqual(goal1.name, "goal1")
        self.assertEqual(goal1.description, "Complete 5 workouts")
        self.assertEqual(goal1.duration, 14)
        self.assertEqual(goal1.daysPerWeek, 3)
        self.assertTrue(goal1.notify)
        self.assertFalse(goal1.completed)

        ## test editGoalName
        goal1.editGoalName("goal01")
        self.assertEqual(goal1.name, "goal01")

        ## test makeProgress
        for i in range(5):
            self.assertFalse(goal1.completed)
            goal1.makeProgress()
            self.assertEqual(goal1.progress, 4-i)

        ## test completed
        self.assertTrue(goal1.completed)

        ## test editGoalDescription
        goal1.editGoalDescription("Complete 3 workouts")
        self.assertEqual(goal1.description,"Complete 3 workouts")

if __name__ == '__main__':
    unittest.main()
