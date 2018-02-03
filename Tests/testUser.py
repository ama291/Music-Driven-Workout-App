#testing example
import unittest
from Scripts.exercise import Exercise
from Scripts.userexercise import UserExercise
from Scripts.user import User

class TestUserExercise(unittest.TestCase):

    def test(self):
        name1 = "Jumping Jacks"
        ex1 = Exercise(name1, 30.0)
        uex1 = UserExercise(ex1, 68.0)
        
        ex2 = Exercise(name1, 30.0)
        uex2 = UserExercise(ex2, 71.0)

        name2 = "High Knees"
        ex3 = Exercise(name2, 30.0)
        uex3 = UserExercise(ex3, 91.0)

        ## test constructor
        usr1 = User("Madeline")
        self.assertEqual(usr1.name, "Madeline")

        ## test trackEx
        usr1.trackEx(uex1)
        self.assertTrue(usr1.exIndexTracked(name1) is not None)
        usr1.trackEx(uex2)
        self.assertEqual(len(usr1.tracked), 1)

        uex2 = UserExercise(ex1, 71.0)
        usr1.trackEx(uex2)
        self.assertTrue(usr1.exIndexTracked(name1) is not None)
        self.assertEqual(len(usr1.tracked), 1)
        self.assertEqual(len(usr1.tracked[0].trials), 3)
        
        ## test untrackEx
        usr1.untrackEx(name1)
        self.assertTrue(usr1.exIndexUntracked(name1) is not None)
        self.assertTrue(usr1.exIndexTracked(name1) is None)

        ## test exIndex
        usr1.trackEx(uex3)
        self.assertEqual(usr1.exIndexTracked(name2), 0)
        usr1.untrackEx(name2)
        self.assertEqual(usr1.exIndexUntracked(name1), 0)
        self.assertEqual(usr1.exIndexUntracked(name2), 1)



if __name__ == '__main__':
    unittest.main()
