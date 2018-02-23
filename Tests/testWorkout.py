import unittest
from Scripts.workout import Workout
from Scripts.exercise import Exercise
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
    themes = None
    categories = ["Cardio", "Stretching"]
    muscleGroups = None
    equipment = ["Body Only"]
    duration = 50
    difficulty = "Intermediate"
    workout1 = usr1.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty)

    # test workout properties match input parameters and has exercises
    self.assertEqual(workout1.uid, usr1.ID)
    self.assertTrue(workout1.duration <= duration) # best duration we could get should not be over input duration
    self.assertEqual(workout1.difficulty, difficulty)
    self.assertEqual(workout1.categories, categories)
    self.assertEqual(workout1.muscleGroups, None)
    self.assertEqual(workout1.currExercise, 0)
    self.assertTrue(len(workout1.Exercises) > 0)
    
    #test exercises in workout are unique
    for i in range(len(workout1.Exercises)):
      for j in range(len(workout1.Exercises)):
        if i != j:
          self.assertFalse(workout1.Exercises[i].name == workout1.Exercises[j].name)
    
    #test duration is within required range
    for i in range(len(workout1.Exercises)):
      self.assertTrue(workout1.Exercises[i].range_start <= workout1.Exercises[i].duration <= workout1.Exercises[i].range_end)
    
    #test if each exercise is from the correct category
    for i in range(len(workout1.Exercises)):
      self.assertTrue(workout1.Exercises[i].category in categories)
      
    #test if each exercise has correct equipment requirement
    for i in range(len(workout1.Exercises)):
      self.assertTrue(workout1.Exercises[i].equipment in equipment)

    # test if each exercise has correct difficulty level
    for i in range(len(workout1.Exercises)):
      self.assertEqual(workout1.Exercises[i].difficulty,difficulty)

    # muscle group condition
    themes = None
    categories = None
    muscleGroups = ["Chest", "Shoulders", "Biceps"]
    equipment = ["Kettlebells", "Machine"]
    duration = 30
    difficulty = "Beginner"
    workout2 = usr1.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty)

    # test workout properties match input parameters and has exercises
    self.assertEqual(workout2.uid, usr1.ID)
    self.assertTrue(workout2.duration <= duration) # best duration we could get should not be over input duration
    self.assertEqual(workout2.difficulty, difficulty)
    self.assertEqual(workout2.categories, None)
    self.assertEqual(workout2.muscleGroups, muscleGroups)
    self.assertEqual(workout2.currExercise, 0)
    self.assertTrue(len(workout2.Exercises) > 0)

    #test array of exercises non empty
    self.assertTrue(len(workout2.Exercises) != 0)
    
    #test exercises in workout are unique
    for i in range(len(workout2.Exercises)):
      for j in range(len(workout2.Exercises)):
        if i != j:
          self.assertFalse(workout2.Exercises[i].name == workout2.Exercises[j].name)

    #test duration is within required range
    for i in range(len(workout2.Exercises)):
      self.assertTrue(workout2.Exercises[i].range_start <= workout2.Exercises[i].duration <= workout2.Exercises[i].range_end)

    #test if each exercise is from the correct muscle group
    for i in range(len(workout2.Exercises)):
      self.assertTrue(workout2.Exercises[i].muscleGroup in muscleGroups)
      
    #test if each exercise has correct equipment requirement
    for i in range(len(workout2.Exercises)):
      self.assertTrue(workout2.Exercises[i].equipment in equipment)
      
    #test if each exercise has correct difficulty level
    for i in range(len(workout2.Exercises)):
      self.assertEqual(workout2.Exercises[i].difficulty,difficulty)
      
      
    '''
    Added Tests for music recommendation
    '''
    #test that duration of music is greater than equal to duration of workout
    duration = 0
    for i in range(len(workout1.getRecommendations)):
      duration += workout1.getRecommendations[i]['duration:']
    self.assertTrue(duration >= workout1.duration)
    
    
    #test that if theme is selected, it is used for getSeeds
    if workout1.theme:
      string = str(workout1.theme['type'])
      self.assertTrue(workout1.theme['name'] in workout1.getSeeds[string])

    #test getSeeds - 1 <= no. of artists+genres+tracks <=5
    self.assertTrue(1 <= len(workout1.getSeeds['artists:']) + len(workout1.getSeeds['genres:']) + len(workout1.getSeeds['tracks:']) <= 5)  


if __name__ == '__main__':
  unittest.main()
