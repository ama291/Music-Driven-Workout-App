import unittest
from Scripts.exercise import Exercise
from Scripts.fitnesstest import FitnessTest

class exampleTest(unittest.TestCase):

    def test(self):
        ## test constructor 
        self.assertRaises(ValueError, FitnessTest, 3, "Toes")
        self.assertRaises(ValueError, FitnessTest, 0, "Cardio")
        ft = FitnessTest("Cardio", 3)
        self.assertEqual(ft.numExercises, 3)
        self.assertEqual(ft.category, "Cardio")

        ## test getRPM
        ex = Exercise("chin-ups", 30.0)
        rpm = ft.getRPM(ex, 14)
        self.assertEqual(rpm, 28.0)

if __name__ == '__main__':
    unittest.main()
