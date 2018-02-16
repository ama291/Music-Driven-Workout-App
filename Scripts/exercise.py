#!/usr/bin/env python3
import random

#Randrange redefined to allow float increments
def randrange(start, stop, step):
    width = stop - start
    n = (width + step - 1) // step
    return start + step * int(random.random() * n)

class Exercise(object):

    def __init__(self, id, name, difficulty, category, muscleGroup, equipment, images, range, increment, rpm):
        self.id = id   
        self.name = name
        self.difficulty = difficulty
        self.category = category
        self.muscleGroup = muscleGroup
        self.equipment = equipment
        self.images = images # list of urls
        self.range_start = range[0]
        self.range_end = range[1]
        self.increment = increment # valid duration increment
        self.duration = randrange(self.range_start, self.range_end, self.increment)
        self.rpm = rpm # either from exercise database or user's fitness test info

    def __repr__(self):
        string = "Exercise: %s for %d seconds" % (self.name, self.duration)
        return string

    def __eq__(self, other):
        return self.id == other.id
        
