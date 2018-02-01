#!/usr/bin/env python2

from exercise import Exercise

class FitnessTest:
	def __init__(self, numExercises, category):
		self.numExercises = numExercises
		self.category = category

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