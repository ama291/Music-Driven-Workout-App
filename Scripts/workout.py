#!/usr/bin/env python3
import uuid

class Workout:
    def __init__(self, uid, categories, muscleGroups, equipment, duration, difficulty):
        self.ID = uuid.uuid4()  # random UUID
        self.uid = uid # user ID, to get fitness test info
        self.categories = categories
        self.muscleGroups = muscleGroups
        self.equipment = equipment
        self.duration = duration
        self.difficulty = difficulty
        self.Exercises = [] # filled by generateWorkout
        self.currExercise = 0 # index of current exercise

    def setCurrEx(self, idx):
        self.currExercise = idx

    def generateWorkout(self):
        """
        Main algorithm goes here:
        Randomly pull exercises from database that match input criteria
        Get proper rpm for each exercise, based on difficulty
        For each exercise, randomly choose duration from its range and increments
        (occurs in exercise constructor, but can reset if need be)
        Use rpm from database or user's fitness test info
        Add to self.Exercises until reach duration (or get close enough)
        """