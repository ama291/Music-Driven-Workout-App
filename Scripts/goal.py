#!/usr/bin/env python3
#from Scripts.user import User
from datetime import datetime

class Goal(object):
    """
    Class for user Goals; goals help users concretely measure their progress
    and feel a sense of achievement.
    Goals are described by what categories e.g. "cardio" and muscleGroups e.g. "biceps" they are in.
    Users can choose to be notified about certain goals and how long the goal will last for.
    """
    def __init__(self, name, description, goalNum, categories,
        muscleGroups, duration, daysPerWeek, notify):
        """
        name: string
        goalNum: integer
        description: string
        duration: int (number of days)
        days per week: int (<=7)
        notifications: boolean
        """
        if(name == "" or name is None):
            raise ValueError("name can't be empty string")
        if(goalNum is None):
            raise ValueError("goalNum can't be None")
        if(goalNum < 0):
            raise ValueError("goalNum can't be less than 0")
        if(duration is None):
            raise ValueError("duration can't be None")
        if(duration < 0):
            raise ValueError("duration can't be less than 0")
        if(daysPerWeek is None):
            raise ValueError("daysPerWeek can't be None")
        if(daysPerWeek < 0):
            raise ValueError("daysPerWeek can't be less than 0")
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
