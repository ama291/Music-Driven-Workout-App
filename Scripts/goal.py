#!/usr/bin/env python3
#from Scripts.user import User
from datetime import datetime

class Goal:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.date = datetime.now()
        self.completed = False

    def __repr__(self):
        string = "Goal: %s: %s - %r" % (self.name, self.description, self.completed)
        return string

    def __eq__(self, other):
        return self.name == other.name

    def goalCompleted(self):
        self.completed = True

    def editGoalName(self, _name):
        self.name = _name

    def editGoalDescription(self, _description):
        self.description = _description
