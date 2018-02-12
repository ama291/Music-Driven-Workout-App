import unittest
from Scripts.exercise import Exercise
from Scripts.userexercise import UserExercise
from datetime import datetime
import json

class TestUserExercise(unittest.TestCase):

    def test(self):
        ## test constructor
        ex1 = Exercise("Calf Raises", 1, "Legs", \
            ["Calves"], ["Stairs"], [], [0,1], 1, 30.0)
        uex1 = UserExercise(ex1, [], [])
        self.assertEqual(uex1.exercise, ex1)
        self.assertEqual(uex1.categories, [])
        self.assertEqual(uex1.trials, [])


        ## test sameExercise
        ex2 = Exercise("Chin-ups", 3, "Arms", \
            ["Bicepts", "Tricepts"], ["Stairs"], [], \
            [0,1], 1, 30.0)
        self.assertTrue(uex1.sameExercise(ex1))
        self.assertFalse(uex1.sameExercise(ex2))
        
        ## test addTrial
        RPMs = [23.5, 32.0, 12.0]
        for t in RPMs:
            uex1.addTrial(datetime.now(), t) 
        self.assertHasRates(uex1, RPMs)
        self.assertEqual(uex1.maxRate[1], 32.0)

        ## test combine
        uex2 = UserExercise(ex2, [], [])
        self.assertRaises(AssertionError, uex1.combine, uex2)
        uex3 = UserExercise(ex1, [], [])
        uex3.addTrial(datetime.now(), 32.5)
        uex3.combine(uex1)
        RPMs.append(32.5)
        self.assertHasRates(uex3, RPMs)

        ## test addFreqFromNumReps 
        time1 = datetime.now()
        uex1.addFreqFromNumReps(time1, 20)
        self.assertTrue((time1, 20 / uex1.exercise.duration * 60) in uex1.trials)

        ## test addFrequency
        filepath = "Logs/log1.json"
        with open(filepath) as f:
            data = json.load(f)
        time2 = datetime.now()
        uex1.addFrequency(time2, data)
        expected1 = (time2, 60.22)
        self.assertTrialAlmostEqual(uex1.trials[4], expected1)

        ## test maxRate
        expected2 = (time1, 1200.)
        self.assertTrialAlmostEqual(uex1.maxRate, expected2)

    def assertHasRates(self, uex, ts):
        for t in ts:
            self.assertTrue(t in uex)

    def assertTrialAlmostEqual(self, t1, t2):
        self.assertEqual(t1[0], t2[0])
        self.assertAlmostEqual(t1[1], t2[1], places=2)

if __name__ == '__main__':
    unittest.main()
