#!/usr/bin/env python3
#from Scripts.user import User

class Theme(object):
    def __init__(self, name, theme, numWorkouts):
        if(name == ""):
            print("name can't be empty string")
            raise ValueError
        if(numWorkouts < 0):
            print("numWorkouts can't be less than 0")
            raise ValueError
        if(theme == ""):
            print("theme can't be empty")
            raise ValueError
        self.name = name
        self.theme = theme
        self.numWorkouts = numWorkouts

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        string = "%s Theme: %s to be used for next %d workouts" % (self.theme, self.name, self.numWorkouts)
        return string

    def editThemeNumWorkouts(self, _numWorkouts):
        if(_numWorkouts < 0):
            print("numWorkouts can't be less than 0")
            return False
        else:
            self.numWorkouts = _numWorkouts
            return True 
