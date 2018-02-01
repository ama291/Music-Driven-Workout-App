#!/usr/bin/env python2

class FitnessTest:
	def __init__(self, numExercises, category):
		self.numExercises = numExercises
		self.category = category

	def __repr__(self):
		string = "FitnessTest: %s, %d exercises" % (self.category, self.numExercises)
		return string		


if __name__ == '__main__':
	test = FitnessTest(3, "cardio")
	print(test)