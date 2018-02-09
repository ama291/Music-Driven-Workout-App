import unittest
from Scripts.workout import Workout
from Scripts.exercise import Exercise
from Scripts.userexercise import UserExercise
from Scripts.user import User


'''
All excercises in the workout must have a different name (using equaliy testing will pass the same excercise with a different duration). 
The list of excercises must be non empty and the sum of their durations should not be more than the user specified duration. 
We will create this list in a greedy manner until the duration is filled up. Each excercise's duration is pulled randomly from a range of 
reasonable durations determined by us and this range is entered by us into the database and saved as an excercise class variable.
'''

class TestWorkout(unittest.TestCase):
  def test(self):
    usr1 = User(1, "Alex", [], [], [], [], [], {}, {})
    #category condition
    duration = 50
    difficulty = "Intermediate"
    categories = ["Cardio", "Strength"]
    workout1 = usr1.getWorkout(duration, difficulty, categories=categories)
    
    #test array of excercises non empty
    assertTrue(len(workout1.Excercises) != 0)
    
    #test excercises in workout are unique 
    for i in range(len(workout1.Excercises)):
      for j in range(len(workout1.Excercises)):
        if i != j:
          self.assertFalse(workout1.Excercises[i].name == workout1.Excercises[j].name)
      
    #test total duration matches or is under user specification
    total_duration = 0
    for i in range(len(workout1.Excercises)):
      total_duration = workout1.Excercises[i].duration + total_duration
    self.assertFalse(total_duration > duration)
    
    #test duration is within required range
    for i in range(len(workout1.Excercises)):
      self.assertTrue(workout1.Excercises[i].range_start <= workout1.Excercises[i].duration <= workout1.Excercises[i].range_end)
    
    
    # muscle group condition
    duration = 30
    difficulty = "Beginner"
    muscleGroups = ["Chest", "Shoulders", "Biceps"]
    workout2 = usr1.getWorkout(duration, difficulty, muscleGroups=muscleGroups)
      
    #test array of excercises non empty
    assertTrue(len(workout2.Excercises) != 0)
    
    #test excercises in workout are unique 
    for i in range(len(workout2.Excercises)):
      for j in range(len(workout2.Excercises)):
        if i != j:
          self.assertFalse(workout2.Excercises[i].name == workout2.Excercises[j].name)
      
    #test total duration matches or is under user specification
    total_duration = 0
    for i in range(len(workout2.Excercises)):
      total_duration = workout2.Excercises[i].duration + total_duration
    self.assertFalse(total_duration > duration)
    
    #test duration is within required range
    for i in range(len(workout2.Excercises)):
      self.assertTrue(workout2.Excercises[i].range_start <= workout2.Excercises[i].duration <= workout2.Excercises[i].range_end)
    
