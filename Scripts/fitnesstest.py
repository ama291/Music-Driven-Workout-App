#!/usr/bin/env python3

from Scripts.exercise import Exercise

class FitnessTest(object):
    def __init__(self, category, numExercises):
        if category not in Exercise.categories:
            raise ValueError("%s is not a valid category")
        if numExercises <= 0:
            raise ValueError("numExercises must be positive")
        self.category = category
        self.numExercises = numExercises

    def __repr__(self):
        string = "FitnessTest: %s, %d exercises" % (self.category, self.numExercises)
        return string

    def getRPM(self, exercise, numReps):
        return numReps * 60.0 / exercise.duration


if __name__ == '__main__':
    test = FitnessTest(3, "cardio")
    print(test)

    ex = Exercise("block jumps", 30.0)

    rpm = test.getRPM(ex, 14)
    print(ex)
    print("rpm: %f" % rpm)