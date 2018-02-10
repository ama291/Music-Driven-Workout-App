#!/usr/bin/env python3
import random

class Exercise(object):

    def __init__(self, name, difficulty, category, muscleGroup, equipment, images, range, increment, rpm):
        self.name = name
        self.difficulty = difficulty
        self.category = category
        self.muscleGroup = muscleGroup
        self.equipment = equipment
        self.images = images # list of urls
        self.range_start = range[0]
        self.range_end = range[1]
        self.increment = increment # valid duration increment
        self.duration = random.randrange(self.range_start, self.range_end, self.increment)
        if self.duration == 0:
            self.duration = 1
        self.rpm = rpm # either from exercise database or user's fitness test info

    def __repr__(self):
        string = "Exercise: %s for %d seconds" % (self.name, self.duration)
        return string

    def __eq__(self, other):
        return self.name == other.name
        
