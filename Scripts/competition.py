#!/usr/bin/env python3
#from Scripts.user import User

class Competition:
    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.date = date
        self.completed = False

    def __repr__(self):
        string = "Competition: %s: %s - %r" % (self.name, self.description, self.date, self.completed)
        return string

    def __eq__(self, other):
        return self.name == other.name

    def competitionCompleted(self):
        self.completed = True

    def editCompetitionName(self, _name):
        self.name = _name

    def editCompetitionDescription(self, _description):
        self.description = _description

    def editCompetitionDate(self, _date):
        self.date = _date
