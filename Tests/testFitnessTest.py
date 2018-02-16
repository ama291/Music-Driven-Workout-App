import unittest
import Scripts.fitnessTest as ft
import json
from random import randint

class TestFitnessTest(unittest.TestCase):

    def test(self):
        yr = randint(1000, 2000)
        ID = randint(2,100000)
        ID2 = randint(2,100000)
        time = "%d-12-12 12:12:12" % yr
        cats = ["Strength"]
        cats2 = ["Strength", "Plyometrics"]

        ## Test count exercise
        self.assertEqual(ft.countExercises("Strength"), 727)

        ## Test getting query string
        q = "SELECT * FROM exercises WHERE type = 'Strength' OR type = 'Plyometrics'"
        self.assertEqual(ft.getExQuery(cats2), q)

        ## Test adding an exercise
        self.assertTrue(ft.addExercise(ID, 12, time, 30.5))
        self.assertFalse(ft.checkTracked(ID, 12))
        self.assertFalse(ft.checkTracked(90243, 12))
        self.assertFalse(ft.checkTracked(ID, 1065))

        ## Test toggle exercise
        self.assertRaises(AssertionError, ft.toggleTracked, 1, 1065)
        self.assertEqual(ft.toggleTracked(ID,12), [ID,12,1])
        self.assertTrue(ft.checkTracked(ID,12))
        self.assertEqual(ft.toggleTracked(ID,12), [ID,12,0])
        self.assertFalse(ft.checkTracked(ID,12))

        ## Test getting tracked exercises
        self.assertEqual(ft.getTrackedExercises(2438983), [])
        exIDs = [12,24,36,48]
        for exID in exIDs:
            ft.addExercise(ID2, exID, time, 64.0)
            ft.toggleTracked(ID2, exID)
        exs = ft.getTrackedExercises(ID2)
        resIDs = list(map(lambda x: x[0], exs))
        self.assertEqual(exIDs, resIDs)
        for exID in resIDs:
            self.assertTrue(ft.checkTracked(ID2, exID))

        ## Test is tracked
        self.assertFalse(ft.checkTracked(ID, 12))
        ft.toggleTracked(ID, 12)
        self.assertTrue(ft.checkTracked(ID, 12))

        ## Test get untractked IDs
        self.assertRaises(AssertionError, ft.getUntrackedIDs, ["fskj"], 3, [])
        self.assertRaises(AssertionError, ft.getUntrackedIDs, cats, -1, [])
        trackedIDs = [23,56]
        IDs = ft.getUntrackedIDs(cats, 4, trackedIDs)
        self.assertEqual(len(IDs), 4)
        for ID in IDs:
            self.assertFalse(ID in trackedIDs)

        ## Test get fitness test
        exIDs = [412,421]
        self.assertRaises(AssertionError, ft.getFitnessTest, ["djfs"], 5, [])
        self.assertRaises(AssertionError, ft.getFitnessTest, cats, -1, [])
        self.assertRaises(AssertionError, ft.getFitnessTest, cats, 1, exIDs)
        tests = ft.getFitnessTest(cats, 5, exIDs)
        self.assertEqual(len(tests), 5)
        IDs = list(map(lambda x: x[0], tests))
        self.assertTrue(412 in IDs)
        self.assertTrue(421 in IDs)
        for t in tests:
            self.assertTrue(t[2] in cats)

        ## Test add motion data
        with open('Logs/log1.json', 'r') as fd:
                data = json.load(fd)
        data = ft.processMotionData(ID, 12, time, data)
        tolerance = 0.1
        actual_rate = (17.0 / 30.0)
        diff = abs(actual_rate - data)
        self.assertTrue(diff < tolerance)
        #TODO: Add check that this is in the database

        ## test getting previous results
        expected = [[139, 1, 144, '2012-12-12 12:12:12', 30.5, 0], [140, 1, 144, '2012-12-12 12:18:12', 30.5, 0]]
        self.assertEqual(ft.getPreviousResults(1, 144), expected)
        self.assertEqual(ft.getPreviousResults(1, 1065), [])

if __name__ == '__main__':
    unittest.main()