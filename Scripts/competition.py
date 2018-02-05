#!/usr/bin/env python3
#from Scripts.user import User

class Competition:
    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.date = date
        self.completed = False
        self.participants = []
        self.exercises = []

    def __repr__(self):
        string = "Competition: %s: %s - %r with participants %s" % (self.name, self.description, self.date, self.completed, self.participants)
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

    def addParticipant(self, _participant):
        if _participant not in participants:
            self.participants.append(_participant)

    def removeParticipant(self, _participant):
        if _participant in participants:
            self.participants.remove(_participant)
        else
            print "This participant doesn't exist"

    # can repeat exercises
    def addExercise(self, _exercise):
        self.exercises.append(_exercise)

    def removeExercise(self, _exercise):
        if _exercise in exercises
            self.exercises.remove(_exercise)
        else _exercise not in exercises
            print "This exercise was not found"
