#!/usr/bin/env python3
from Scripts.workout import Workout
import requests

dbURL = "http://138.197.49.155:8000/api/database/"
key = "SoftCon2018"

class User(object):
    def __init__(self, ID, name, tracked, untracked, goals,
         themes, competitions, inProgressWorkouts, savedWorkouts):
        self.ID = ID
        self.name = name
        self.tracked = tracked
        self.untracked = untracked
        self.goals = goals
        self.themes = themes
        self.competitions = competitions

        # stores current and incomplete workouts
        self.inProgressWorkouts = inProgressWorkouts # key: workoutID, value: workout class instance
        # stores saved workouts, if a user wants to do the workout again
        self.savedWorkouts = savedWorkouts # key: workoutID, value: workout class instance

    def __repr__(self):
        string = "User: %s\n***\nTracked:" % self.name
        for ex in self.tracked:
            string += "\n%s" % str(ex)
        string += "\n***\nUntracked:"
        for ex in self.untracked:
            string += "\n%s" % str(ex)
        string += "\n***"
        return string

    def getFitnessTest(self, categories, numExercises, tracked):
        numUntracked = numExercises - len(tracked)
        ## TODO: get numUntracked exercises from the database
        #  that are neither tracked nor (saved) untracked for the user.
        #  Create a UserExercise for each exercise.
        return []

    def exIndexTracked(self, name):
        count = 0
        for uex in self.tracked:
            if uex.exercise.name == name:
                return count
            count += 1
        return None

    def exIndexUntracked(self, name):
        count = 0
        for uex in self.untracked:
            if uex.exercise.name == name:
                return count
            count += 1
        return None

    def hasEx(self, name):
        return self.exIndexTracked(name) is not None \
         or self.exIndexUntracked(name) is not None

    def trackEx(self, userexercise):
        """
        checks if the user is already tracking the exercise. If so,
        it adds the new info. If not, it adds it to tracked exercises.
        If it's in the untracked exercises, it moves the untracked
        exercise with the same name to tracked exercises.
        """
        exname = userexercise.exercise.name
        idx = self.exIndexTracked(exname)
        if idx is not None:
            self.tracked[idx].combine(userexercise)
        elif self.exIndexUntracked(exname) is None:
            self.tracked.append(userexercise)
        else:
            idx = self.exIndexUntracked(exname)
            uex = self.untracked[idx]
            del self.untracked[idx]
            uex.combine(userexercise)
            self.tracked.append(uex)

    def untrackEx(self, name):
        """
        moves the UserExercise by the given name from tracked to auntracked
        """
        idx = self.exIndexTracked(name)
        assert idx is not None
        uex = self.tracked[idx]
        del self.tracked[idx]
        self.untracked.append(uex)

    def getWorkout(self, themes, categories, muscleGroups, equipment, duration, difficulty):
        """
        User either inputs a list of categories or a list of muscle groups
        Returns a workout based in the user's inputs

        Note: checking that duration, difficulty, equipment, and categories
        or muscleGroups are non-empty done by the app (can have no theme applied)

        Note: categories and muscleGroups options come from user's goals
        (can select any number, at least 1, but either categories or
        muscleGroups, not both), themes options come from user's themes
        (select up to 5, at least 1), equipment options based on exercise
        database (select any number, at least 1), difficulty options based
        on exercise database (select 1), and duration options set by us
        (select 1)
        """

        # TODO (next iteration): handle themes
        """
        for theme in themes:
            t = self.themes[theme.ID]
            t.timesUsed += 1
            if t.timesUsed == t.numWorkouts:
                del self.themes[theme.ID]
            else:
                self.themes[theme.ID] = t
        """
        new = Workout(self.ID, themes, categories, muscleGroups,
                      equipment, duration, difficulty)
        hasGenerated = new.generateWorkout() # true if no request failures
        return new if hasGenerated else None

    def startWorkout(self, workout):
        id = workout.ID

        if id not in self.inProgressWorkouts:
            self.inProgressWorkouts[id] = workout
            return True

        return False

    def startSavedWorkout(self, id):
        if id in self.savedWorkouts and id not in self.inProgressWorkouts:
            workout = self.savedWorkouts[id]
            self.inProgressWorkouts[id] = workout
            return True

        return False

    def quitWorkout(self, id):
        """
        NOTE: can also be used when the user has completed
        a workout and does not want to save it
        """
        if id in self.inProgressWorkouts:
            del self.inProgressWorkouts[id]
            return True

        return False

    def pauseWorkout(self, id, pausedOn):
        """
        NOTE: will start at this exercise when workout is resumed
        """
        if id in self.inProgressWorkouts:
            workout = self.inProgressWorkouts[id]
            workout.setCurrEx(pausedOn)
            self.inProgressWorkouts[id] = workout
            return True

        return False

    def saveWorkout(self, id):
        if id in self.inProgressWorkouts and id not in self.savedWorkouts:
            toSave = self.inProgressWorkouts[id]
            toSave.setCurrEx(0) # roll back workout to beginning
            self.savedWorkouts[id] = toSave
            del self.inProgressWorkouts[id]
            return True

        return False

    def unsaveWorkout(self, id):
        if id in self.savedWorkouts:
            if id in self.inProgressWorkouts:
                del self.inProgressWorkouts[id]
            del self.savedWorkouts[id]
            return True

        return False

    def workoutsInProgress(self):
        """
        Return all incomplete workouts so the app can load them for a user to see
        From there the user can resume a workout, which should start at the paused exercise
        NOTE: can also be retrieved directly from database
        """
        return self.inProgressWorkouts

    def workoutsSaved(self):
        """
        Return all saved workouts so the app can load them for a user to see
        From there the user can restart a workout, which should start at the first exercise
        Unless it has an in progress version, in which case the app should redirect them
        NOTE: can also be retrieved directly from database
        """
        return self.savedWorkouts

    def addGoal(self, goal):
        self.goals.append(goal)

    def removeGoal(self, goal):
        if goal in self.goals:
            self.goals.remove(goal)
            return True
        return False

    def addTheme(self, theme):
        if(theme in self.themes):
            print("duplicate theme!")
            return False
        else:
            self.themes.append(theme)
            return True 

    def removeTheme(self, theme):
        if theme in self.themes:
            self.themes.remove(theme)
            return True
        return False

    def addCompetition(self, competition):
        self.competitions.append(competition)

    def removeCompetition(self, competition):
        if competition in self.competitions:
            self.competitions.remove(competition)
            return True
        return False
