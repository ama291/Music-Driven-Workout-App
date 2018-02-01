#!/usr/bin/env python2

class Exercise:
	def __init__(self, name, duration):
		self.name = name
		self.duration = duration

	def __repr__(self):
		string = "Exercise: %s for %f seconds" % (self.name, self.duration)
		return string
		
if __name__ == '__main__':
	ex = Exercise("chin-ups", 30.0)
	print(ex)