#!/usr/bin/env python3
import uuid

class Workout:
    def __init__(self, categories, muscleGroups, duration, difficulty):
        self.ID = uuid.uuid4()  # random UUID
        self.categories = categories
        self.muscleGroups = muscleGroups
        self.duration = duration
        self.difficulty = difficulty
        self.Exercises = [] # filled by generateWorkout
        self.currExercise = 0 # index of current exercise

    def getID(self):
        return self.ID

    def setCurrEx(self, idx):
        self.currExercise = idx

    def generateWorkout(self):
        """
        Main algorithm goes here:
        Randomly pull exercises from database that match input criteria
        Get proper rpm for each exercise, based on difficulty
        For each exercise, randomly choose duration from its range and increments
        (range either from the database or the user)
        Add to self.Exercises until reach duration (or get close)
        """