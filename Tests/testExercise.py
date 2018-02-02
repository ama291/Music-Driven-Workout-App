#testing example
import unittest
from Scripts.exercise import Exercise

class TestExercise(unittest.TestCase):

    def test(self):
    	## test constructor
        ex = Exercise("Chin-ups", 30.0)
        self.assertEqual(ex.name, "Chin-ups")
        self.assertEqual(ex.duration, 30.0)

if __name__ == '__main__':
    unittest.main()
