import unittest
from Scripts.workout import Workout
from Scripts.exercise import Exercise
from Scripts.user import User
from Scripts.theme import Theme

'''
All excercises in the workout must have a different name (using equaliy testing will pass the same excercise with a different duration).
The list of excercises must be non empty and the sum of their durations should not be more than the user specified duration.
We will create this list in a greedy manner until the duration is filled up. Each excercise's duration is pulled randomly from a range of
reasonable durations determined by us and this range is entered by us into the database and saved as an excercise class variable.
'''

class TestWorkout(unittest.TestCase):
  def test(self):
    usr1 = User(1, "Alex", 167, 150, 1996, [], [], [], {}, {})
    accessToken = "example-access-token"

    #category condition
    theme1 = Theme("The Killers", "artist", "0C0XlULifJtAgn6ZNCW2eu", 1)
    theme2 = Theme("Zion & Lennox", "artist", "21451j1KhjAiaYKflxBjr1", 2)
    theme3 = Theme("Otra Vez (feat. J Balvin)", "track", "7pk3EpFtmsOdj8iUhjmeCM", 3)
    theme4 = Theme("Disciples", "track", "2gNfxysfBRfl9Lvi9T3v6R", 4)
    theme5 = Theme("Hip Hop", "genre", "hip_hop", 5)
    themes = [theme1, theme2, theme3, theme4, theme5]
    categories = ["Cardio", "Stretching"]
    muscleGroups = None
    equipment = ["Body Only"]
    duration = 50
    difficulty = "Intermediate"
    workout1 = usr1.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)

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
    #for i in range(len(workout1.Exercises)):
    #  self.assertTrue(workout1.Exercises[i].range_start <= workout1.Exercises[i].duration <= workout1.Exercises[i].range_end)

    #test if each exercise is from the correct category
    for i in range(len(workout1.Exercises)):
      self.assertTrue(workout1.Exercises[i].category in categories)

    #test if each exercise has correct equipment requirement
    for i in range(len(workout1.Exercises)):
      self.assertTrue(workout1.Exercises[i].equipment in equipment)

    # test if each exercise has correct difficulty level
    # for i in range(len(workout1.Exercises)):
    #  self.assertEqual(workout1.Exercises[i].difficulty,difficulty)

    # muscle group condition
    themes = None
    categories = None
    muscleGroups = ["Chest", "Shoulders", "Biceps"]
    equipment = ["Kettlebells", "Machine"]
    duration = 30
    difficulty = "Beginner"
    workout2 = usr1.getWorkout(themes, categories, muscleGroups, equipment, duration, difficulty, accessToken)

    # test workout properties match input parameters and has exercises
    self.assertEqual(workout2.uid, usr1.ID)
    self.assertTrue(workout2.duration <= duration) # best duration we could get should not be over input duration
    # self.assertEqual(workout2.difficulty, difficulty)
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
    #for i in range(len(workout2.Exercises)):
    #  self.assertTrue(workout2.Exercises[i].range_start <= workout2.Exercises[i].duration <= workout2.Exercises[i].range_end)

    #test if each exercise is from the correct muscle group
    for i in range(len(workout2.Exercises)):
      self.assertTrue(workout2.Exercises[i].muscleGroup in muscleGroups)

    #test if each exercise has correct equipment requirement
    for i in range(len(workout2.Exercises)):
      self.assertTrue(workout2.Exercises[i].equipment in equipment)

    #test if each exercise has correct difficulty level
    #for i in range(len(workout2.Exercises)):
    #  self.assertEqual(workout2.Exercises[i].difficulty,difficulty)


    '''
    Added Tests for music recommendation
    '''
    # NOTE - can't do these this because don't have valid accessToken
    # #test that duration of music is greater than equal to duration of workout
    # for i in range(len(workout1.Exercises)):
    #   result = workout1.getRecommendations(workout1.spotID, workout1.themes, workout1.accessToken, workout1.Exercises[i].bpm, workout1.Exercises[i].duration)
    #   duration = 0
    #   for j in range(len(result)):
    #     duration += result[j]['duration']
    #   self.assertTrue(duration >= workout1.Exercises[i].duration)

    # NOTE - can do this test because won't use the invalid accessToken
    # test that if selected, themes are used for getSeeds
    seeds = workout1.getSeeds(workout1.spotID, workout1.themes, workout1.accessToken)
    if workout1.themes:
        for theme in workout1.themes:
            themeUsed = False
            for key in seeds:
                if theme.spotifyId in seeds[key]:
                    themeUsed = True
                    break
            self.assertTrue(themeUsed)

    #test getSeeds - no. of artists+genres+tracks <=5
    # with themes
    artist_len = 0 if seeds['artists'] is None else len(seeds['artists'])
    genres_len = 0 if seeds['genres'] is None else len(seeds['genres'])
    tracks_len = 0 if seeds['tracks'] is None else len(seeds['tracks'])
    self.assertTrue(artist_len + genres_len + tracks_len <= 5)
    # without themes
    seeds = workout2.getSeeds(workout2.spotID, workout2.themes, workout2.accessToken)
    artist_len = 0 if seeds['artists'] is None else len(seeds['artists'])
    genres_len = 0 if seeds['genres'] is None else len(seeds['genres'])
    tracks_len = 0 if seeds['tracks'] is None else len(seeds['tracks'])
    self.assertTrue(artist_len + genres_len + tracks_len <= 5)

    # NOTE - can't include this test yet
    # #test getBPM which gets bpm from rpm
    # for i in range(len(workout1.Exercises)):
    #   rpm = workout1.Exercises[i].rpm
    #   bpm = workout1.getBPM(rpm,min_beats,max_beats)
    #   self.assertTrue(min_beats <= bpm <= max_beats )  #bpm is within required range
    #   self.assertTrue((bpm % rpm) == 0)   #bpm is multiple of rpm


if __name__ == '__main__':
  unittest.main()
