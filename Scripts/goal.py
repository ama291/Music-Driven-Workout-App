#!/usr/bin/env python3
#from Scripts.user import User
from datetime import datetime

class Goal(object):
    def __init__(self, name, description, startingProgress, duration, daysPerWeek, notify):
        """
        name: string
        description: string
        duration: int (number of days)
        days per week: int (<=7)
        notifications: boolean
        """
        self.name = name
        self.description = description
        self.progress = startingProgress
        self.date = datetime.now()
        self.duration = duration
        self.daysPerWeek = daysPerWeek
        self.notify = notify

    def __repr__(self):
        string = "Goal: %s: %s - %r" % (self.name, self.description, self.completed)
        return string

    def __eq__(self, other):
        return self.name == other.name

    def makeProgress(self):
        self.progress -= 1

    @property
    def completed(self):
        return self.progress <= 0

    def editGoalName(self, _name):
        self.name = _name

    def editGoalDescription(self, _description):
        self.description = _description
