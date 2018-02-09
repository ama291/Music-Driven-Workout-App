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
        self.winners = [] #multiple winners in case of ties

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
        if _participant not in self.participants:
            self.participants.append(_participant)
            return True
        else:
            return False

    def removeParticipant(self, _participant):
        if _participant in self.participants:
            self.participants.remove(_participant)
            return True
        else:
            print ("This participant doesn't exist")
            return False

    # can repeat exercises
    def addExercise(self, _exercise):
        self.exercises.append(_exercise)

    def removeExercise(self, _exercise):
        if _exercise in self.exercises:
            self.exercises.remove(_exercise)
            return True
        elif _exercise not in self.exercises:
            print ("This exercise was not found")
            return False

    def declareWinners(self, _winner):
        if _winner not in self.winners:
            self.winners.append(_winner)
            return True
        else:
            return False
