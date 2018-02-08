import unittest
from Scripts.exercise import Exercise
from Scripts.userexercise import UserExercise

class TestUserExercise(unittest.TestCase):

    def test(self):
        ## test constructor
        ex1 = Exercise("Lunges", 30.0)
        uex1 = UserExercise(ex1, 32.0)
        self.assertEqual(uex1.exercise, ex1)
        self.assertEqual(uex1.trials[0][1], 32.0)

        ## test sameExercise
        ex2 = Exercise("Frog Jumps", 20.0)
        self.assertTrue(uex1.sameExercise(ex1))
        self.assertFalse(uex1.sameExercise(ex2))
        
        ## test addTrial
        RPMs = [23.5, 32.0, 12.0]
        for t in RPMs:
            uex1.addTrial(t) 
        self.assertHasRates(uex1, RPMs)
        self.assertEqual(uex1.maxRate[1], 32.0)

        ## test combine
        uex2 = UserExercise(ex2, 35.2)
        self.assertRaises(AssertionError, uex1.combine, uex2)
        uex3 = UserExercise(ex1, 32.5)
        uex3.combine(uex1)
        RPMs.append(32.5)
        self.assertHasRates(uex3, RPMs)

    def assertHasRates(self, uex, ts):
        for t in ts:
            self.assertTrue(t in uex)

if __name__ == '__main__':
    unittest.main()
