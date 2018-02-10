#testing example
import unittest
from Scripts.goal import Goal
from Scripts.user import User

class TestGoal(unittest.TestCase):

    def test(self):
        goal1 = Goal("goal1", "Complete 1 workout")
        goal2 = Goal("goal2","Complete 5 workouts")
        goal2.addCategory('workouts')
        goal2.addMuscleGroup('cardio')

        ## test constructor
        self.assertEqual(goal1.name, "goal1")
        self.assertEqual(goal2.description, "Complete 5 workouts")

        #test getCategories
        self.assertEqual(goal2.getCategories(), ['workouts'])
        self.assertEqual(goal1.getCategories(), [])

        #test getMuscleGroups
        self.assertEqual(goal2.getMuscleGroups(), ['cardio'])
        self.assertEqual(goal1.getMuscleGroups(), [])

        ## test editGoalDescription
        goal2.editGoalDescription("Complete 3 workouts")
        self.assertEqual(goal2.description,"Complete 3 workouts")

if __name__ == '__main__':
    unittest.main()
