import unittest
import Scripts.fitnessTest as ft
from random import randint

class TestFitnessTest(unittest.TestCase):

    def test(self):
        yr = randint(1000, 2000)
        ID = randint(2,100000)
        time = "%d-12-12 12:12:12" % yr
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
        cats = ["Strength"]
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
            print(t)
            self.assertTrue(t[2] in cats)

if __name__ == '__main__':
    unittest.main()