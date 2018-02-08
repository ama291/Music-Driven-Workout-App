import unittest
from Scripts.goal import Goal
from Scripts.user import User

class TestGoal(unittest.TestCase):

    def test(self):
        goal1 = Goal("goal1", "Complete 1 workout")
        goal2 = Goal("goal2","Complete 5 workouts")

        ## test constructor
        self.assertEqual(goal1.name, "goal1")
        self.assertEqual(goal2.description, "Complete 5 workouts")
        self.assertFalse(goal2.completed)

        ## test goalCompleted
        goal1.goalCompleted()
        self.assertTrue(goal1.completed)

        ## test editGoalName
        goal1.editGoalName("goal01")
        self.assertEqual(goal1.name, "goal01")

        ## test editGoalDescription
        goal2.editGoalDescription("Complete 3 workouts")
        self.assertEqual(goal2.description,"Complete 3 workouts")

if __name__ == '__main__':
    unittest.main()
