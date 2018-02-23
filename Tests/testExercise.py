import unittest
from Scripts.exercise import Exercise
import random

class TestExercise(unittest.TestCase):

    def test(self):
    	## test constructor
        ex1 = Exercise(1, "Calf Raises", "Intermediate", "Legs",
            "Calves", "Stairs", "image1.png", [10,60], 1, 30.0, 140.0)
        self.assertEqual(ex1.name, "Calf Raises")
        self.assertEqual(ex1.difficulty, "Intermediate")
        self.assertEqual(ex1.category, "Legs")
        self.assertEqual(ex1.muscleGroup, "Calves")
        self.assertEqual(ex1.equipment, "Stairs")
        self.assertEqual(ex1.images, "image1.png")
        self.assertEqual(ex1.range_start, 10)
        self.assertEqual(ex1.range_end, 60)
        self.assertLessEqual(ex1.duration, 60)
        self.assertGreaterEqual(ex1.duration, 10)
        self.assertEqual(ex1.increment, 1)
        self.assertEqual(ex1.rpm, 30.0)
        self.assertEqual(ex1.bpm, 140.0)

        ## test equality
        ex2 = Exercise(1, "Calf Raises", "Intermediate", "Legs",
            "Calves", "Stairs", "image2.png", [4,60], 1, 20.0, 160.0)
        ex3 = Exercise(3, "Chin-ups", "Intermediate", "Arms",
            "Biceps", "Stairs", "image1.png",
            [0,1], 1, 30.0, 170.0)
        self.assertTrue(ex1 == ex2)
        self.assertFalse(ex1 == ex3)

if __name__ == '__main__':
    unittest.main()
