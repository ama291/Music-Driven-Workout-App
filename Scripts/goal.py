#!/usr/bin/env python3
#from Scripts.user import User
from datetime import datetime

class Goal(object):
    def __init__(self, name, description, goalNum, categories, \
        muscleGroups, duration, daysPerWeek, notify):
        """
        name: string
        description: string
        duration: int (number of days)
        days per week: int (<=7)
        notifications: boolean
        """
        self.name = name
        self.description = description
        self.progress = 0
        self.goalNum = goalNum
        self.date = datetime.now()
        self.duration = duration
        self.daysPerWeek = daysPerWeek
        self.notify = notify
        self.categories = categories
        self.muscleGroups = muscleGroups

    def __repr__(self):
        string = "Goal: %s: %s - %s, %s" % (self.name, self.description, self.categories, self.muscleGroups)
        return string

    def __eq__(self, other):
        return self.name == other.name

    def makeProgress(self):
        self.progress += 1

    @property
    def completed(self):
        return self.progress >= self.goalNum

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
