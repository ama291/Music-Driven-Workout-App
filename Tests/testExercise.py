#testing example
import unittest
from Scripts.exercise import Exercise

class TestExercise(unittest.TestCase):

    def test(self):
    	## test constructor
        ex1 = Exercise("Chin-ups", 30.0)
        self.assertEqual(ex1.name, "Chin-ups")
        self.assertEqual(ex1.duration, 30.0)

        ex2 = Exercise("Chin-ups", 20.0)
        ex3 = Exercise("Pull-ups", 30.0)
        self.assertTrue(ex1 == ex2)
        self.assertFalse(ex1 == ex3)

if __name__ == '__main__':
    unittest.main()
