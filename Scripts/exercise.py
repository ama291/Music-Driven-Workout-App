#!/usr/bin/env python3

class Exercise:
    categories = ["Cardio", "Arms", "Abs"]

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def __repr__(self):
        string = "Exercise: %s for %f seconds" % (self.name, self.duration)
        return string

    def __eq__(self, other):
        return self.name == other.name
        
if __name__ == '__main__':
    ex = Exercise("chin-ups", 30.0)
    print(ex)