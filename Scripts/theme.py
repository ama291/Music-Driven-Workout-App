#!/usr/bin/env python3
#from Scripts.user import User

class Theme(object):
    def __init__(self, name, theme, numWorkouts):
        self.name = name
        self.theme = theme
        self.numWorkouts = numWorkouts

    def __repr__(self):
        string = "%s Theme: %s to be used for next %n workouts" % (self.theme, self.name, self.numWorkouts)
        return string

    def editThemeNumWorkouts(self, _numWorkouts):
        self.numWorkouts = _numWorkouts
