#!/usr/bin/env python3
#from Scripts.user import User
from datetime import datetime

class Goal:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.date = datetime.now()
        self.categories = []
        self.muscleGroups = []

    def __repr__(self):
        string = "Goal: %s: %s - %s, %s" % (self.name, self.description, self.categories, self.muscleGroups)
        return string

    def __eq__(self, other):
        return self.name == other.name

    def addCategory(self, _cat):
        self.categories.append(_cat)

    def addMuscleGroup(self, _mg):
        self.muscleGroups.append(_mg)

    def getCategories(self):
        return self.categories

    def getMuscleGroups(self):
        return self.muscleGroups

    def editGoalDescription(self, _description):
        self.description = _description
