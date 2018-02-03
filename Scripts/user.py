#!/usr/bin/env python3
from Scripts.exercise import Exercise
from Scripts.userexercise import UserExercise
from Scripts.fitnesstest import FitnessTest
from Scripts.workout import Workout # added by Larissa

class User:
    def __init__(self, name):
        self.name = name
        self.tracked = []
        self.untracked = []

        # added by Larissa
        # stores current and incomplete workouts
        self.inProgressWorkouts = {} # key: workoutID, value: workout class instance
        # stores saved workouts, if a user wants to do the workout again
        self.savedWorkouts = {} # key: workoutID, value: workout class instance

    def __repr__(self):
        string = "User: %s\n***\nTracked:" % self.name
        for ex in self.tracked:
            string += "\n%s" % str(ex)
        string += "\n***\nUntracked:"
        for ex in self.untracked:
            string += "\n%s" % str(ex)
        string += "\n***"
        return string

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

    def testFitness(self, category, numExercises):
        test = FitnessTest(category, numExercises)

    # added by Larissa
    def getWorkout(self, duration, difficulty, categories = None, muscleGroups = None):
        """
        User either inputs a list of categories or a list of muscle groups
        Returns a workout based in the user's inputs
        """
        new = Workout(categories, muscleGroups, duration, difficulty)
        new.generateWorkout()
        return new

    def startWorkout(self, workout):
        self.inProgressWorkouts[workout.getID()] = workout

    def quitWorkout(self, id):
        """
        NOTE: can also be used when the user has completed
        a workout and does not want to save it
        :param id: workout ID
        """
        del self.inProgressWorkouts[id]

    def pauseWorkout(self, id, pausedOn):
        """
        Updates in progress workout to the paused exercise
        Will start at this exercise when workout is resumed
        :param id: workout ID
        :param pausedOn: exercise where pause occurred
        """
        workout = self.inProgressWorkouts[id]
        workout.setCurrEx(pausedOn)
        self.inProgressWorkouts[id] = workout

    def saveWorkout(self, id):
        """
        Upon completing a workout, user can save it
        :param id: workout ID
        """
        toSave = self.inProgressWorkouts[id]
        toSave.setCurrEx(0) # roll back workout to beginning
        self.savedWorkouts[id] = toSave
        del self.inProgressWorkouts[id]

    def unsaveWorkout(self, id):
        del self.savedWorkouts[id]

    def workoutsInProgress(self):
        """
        Return all incomplete workouts so the app can load them for a user to see
        From there the user can resume a workout, which should start at the paused exercise
        """
        return self.inProgressWorkouts

    def workoutsSaved(self):
        """
        Return all saved workouts so the app can load them for a user to see
        From there the user can restart workout, which should start at the first exercise
        """
        return self.savedWorkouts

if __name__ == '__main__':
    user = User("Madeline")
    print(user)