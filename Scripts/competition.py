#!/usr/bin/env python3
#from Scripts.user import User

class Competition(object):
    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.date = date
        self.completed = False
        self.participants = {} #key =  user id, value = score
        self.exercises = []
        self.winners = [] #multiple winners in case of ties

    def __repr__(self):
        string = "Competition: %s: %s - %r %r with participants %s" % (self.name, self.description, self.date, self.completed, self.participants)
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

    def addParticipant(self, _participant): #_participant = user id
        if _participant not in self.participants:
            self.participants[_participant] = 0
            return True
        else:
            return False

    def removeParticipant(self, _participant):
        if _participant in self.participants:
            self.participants.pop(_participant, None)
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

    def findWinner(self):
        maxVal = max(self.participants, key=self.participants.get)
        for i in self.participants:
            if self.participants[i] == self.participants[maxVal]:
                self.winners.append(i)
        return self.winners

    def getNumParticipants(self):
        return len(self.participants)
