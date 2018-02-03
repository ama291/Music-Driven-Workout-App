#!/usr/bin/env python3
from Scripts.exercise import Exercise
from Scripts.userexercise import UserExercise
from Scripts.fitnesstest import FitnessTest

class User:
    def __init__(self, name):
        self.name = name
        self.tracked = []
        self.untracked = []

    def __repr__(self):
        string = "User: %s\n***\nTracked:" % self.name
        for ex in self.tracked:
            string += "\n%s" % str(ex)
        string += "\n***\nUntracked:"
        for ex in self.untracked:
            string += "\n%s" % str(ex)
        string += "\n***"
        return string

    def exIndexTracked(self, name):
        count = 0
        for uex in self.tracked:
            if uex.exercise.name == name:
                return count
            count += 1
        return None

    def exIndexUntracked(self, name):
        count = 0
        for uex in self.untracked:
            if uex.exercise.name == name:
                return count
            count += 1
        return None

    def hasEx(self, name):
        return self.exIndexTracked(name) is not None \
         or self.exIndexUntracked(name) is not None

    def trackEx(self, userexercise):
        """
        checks if the user is already tracking the exercise. If so,
        it adds the new info. If not, it adds it to tracked exercises.
        If it's in the untracked exercises, it moves the untracked 
        exercise with the same name to tracked exercises.
        """
        exname = userexercise.exercise.name
        idx = self.exIndexTracked(exname)
        if idx is not None:
            self.tracked[idx].combine(userexercise)
        elif self.exIndexUntracked(exname) is None:
            self.tracked.append(userexercise)
        else:
            idx = self.exIndexUntracked(exname)
            uex = self.untracked[idx]
            del self.untracked[idx]
            uex.combine(userexercise)
            self.tracked.append(uex)

    def untrackEx(self, name):
        """
        moves the UserExercise by the given name from tracked to auntracked
        """
        idx = self.exIndexTracked(name)
        assert idx is not None
        uex = self.tracked[idx]
        del self.tracked[idx]
        self.untracked.append(uex)


    def testFitness(self, category, numExercises):
        test = FitnessTest(category, numExercises)


if __name__ == '__main__':
    user = User("Madeline")
    print(user)