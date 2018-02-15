import unittest
import Scripts.fitnessTest as ft
import json
from random import randint

class TestFitnessTest(unittest.TestCase):

    def test(self):
        yr = randint(1000, 2000)
        ID = randint(2,100000)
        time = "%d-12-12 12:12:12" % yr
        cats = ["Strength"]
        cats2 = ["Strength", "Plyometrics"]

        ## Test count exercise
        self.assertEqual(ft.countExercises("Strength"), 859)

        ## Test getting query string
        q = "SELECT * FROM exercises WHERE type = 'Strength' OR type = 'Plyometrics'"
        self.assertEqual(ft.getExQuery(cats2), q)

        ## Test adding an exercise
        self.assertEqual(ft.addExercise(ID, 12, time, 30.5), "OK")
        self.assertFalse(ft.checkTracked(ID, 12))

        ## Test toggle exercise
        self.assertEqual(ft.toggleTracked(ID,12), [ID,12,1])
        self.assertTrue(ft.checkTracked(ID,12))
        self.assertEqual(ft.toggleTracked(ID,12), [ID,12,0])
        self.assertFalse(ft.checkTracked(ID,12))

        ## Test is tracked
        self.assertEqual(ft.isTracked(ID, 12), "False")
        ft.toggleTracked(ID, 12)
        self.assertEqual(ft.isTracked(ID, 12), "True")

        ## Test get untrectked IDs
        trackedIDs = [23,56]
        IDs = ft.getUntrackedIDs(cats, 4, trackedIDs)
        self.assertEqual(len(IDs), 4)
        for ID in IDs:
            self.assertFalse(ID in trackedIDs)

        ## Test get fitness test
        tests = ft.getFitnessTest(cats, 5, [412,421])
        self.assertEqual(len(tests), 5)
        IDs = map(lambda x: x[0], tests)
        self.assertTrue(412 in IDs)
        self.assertTrue(421 in IDs)
        for t in tests:
            self.assertTrue(t[2] in cats)

        ## Test add motion data
        with open('Logs/log1.json', 'r') as fd:
                data = json.load(fd)
        data = processMotionData(ID, 12, time, data)
        tolerance = 0.1
        actual_rate = (17.0 / 30.0)
        diff = abs(actual_rate - data)
        self.assertTrue(diff < tolerance)

if __name__ == '__main__':
    unittest.main()