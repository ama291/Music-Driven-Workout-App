#!/usr/bin/env python3
from Scripts.exercise import Exercise
from Scripts.log import Log
from datetime import datetime

class UserExercise:
    def __init__(self, exercise, categories, trials):
        self.exercise = exercise
        self.categories = categories
        self.trials = trials

    def __repr__(self):
        string = "UserExercise: %s, max: %f rpm on %s\n\tTrials:" % \
         (self.exercise.name, self.maxRate[1], str(self.maxRate[0]))
        for time, rate in self.trials:
            string += "\n\t\t %f rpm on %s" % (rate, str(time))
        return string

    def __contains__(self, rpm):
        for time, rate in self.trials:
            if rate == rpm:
                return True
        return False

    def sameExercise(self, exercise):
        return self.exercise == exercise

    def combine(self, other):
        assert(self.exercise == other.exercise)
        self.trials += other.trials
        self.trials.sort()

    def addTrial(self, date, freq):
        self.trials.append((date, freq))

    def addFreqFromNumReps(self, time, numReps):
        freq = numReps * 60.0 / self.exercise.duration
        self.addTrial(time, freq)

    def addFrequency(self, time, data):
        log = Log(data)
        freq = log.getFrequency()
        self.addTrial(time, freq)

    @property
    def maxRate(self):
        return(max(self.trials, key=lambda x: x[1]))

if __name__ == '__main__':
    ex = Exercise("Lunges", 30.0)
    uex = UserExercise(ex, 16.0, 12)
    for i in [23.5,32.0,12.0]:
        uex.addTrial(i)
    print(uex)
    print(uex.maxRate)
