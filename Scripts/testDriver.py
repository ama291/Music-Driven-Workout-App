from Scripts.driver import *
from Scripts.exercise import Exercise
import uuid

class testWorkout(object):
    def __init__(self, uid, themes, categories, muscleGroups, equipment, duration, difficulty):
        self.ID = str(uuid.uuid4())  # random UUID
        self.themes = themes # will not be used until iter 2, for music recommendations
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

#workout1 = testWorkout(0, None, ["Cardio", "Strength"], None, ["Body Only"], 50, "Advanced")
#ret = startWorkout(0, workout1)
#print(ret)

"""query = 'SELECT * FROM users where id = %s' % str(0)
r = requests.post('http://138.197.49.155:8000/api/database/', data = {'query': query, 'key': 'SoftCon2018'})
print(r.json())"""

attributes = ['name', 'type', 'muscle', 'level', 'equipment, range_start, range_end, increment, rpm']
query = 'SELECT %s FROM exercises WHERE type IN (\'Cardio\', \'Stretching\') AND equipment \
        IN (\'Body Only\') AND level = \'Beginner\' ORDER BY RANDOM() LIMIT 10' % (', '.join(attributes))
query = 'select * from users'
r = requests.post('http://138.197.49.155:8000/api/database/',
                    data={'query': query, 'key': 'SoftCon2018'})
print(r.json())

"""m, n = len(dbExercises), len(ordering)
exercises = []
total_duration = 0

for i in range(m):

    for j in range(n):
        if ordering[j] == "name":
            name = dbExercises[i][j]
        elif ordering[j] == "level":
            difficulty = dbExercises[i][j]
        elif ordering[j] == "type":
            category = dbExercises[i][j]
        elif ordering[j] == "muscle":
            muscleGroup = dbExercises[i][j]
        elif ordering[j] == "equipment":
            equipment = dbExercises[i][j]

    new = Exercise(name, difficulty, category, muscleGroup, equipment, [], [2, 10], 2, 60)

    if new.duration + total_duration <= durr:
        exercises.append(new)
        total_duration += new.duration
        if total_duration == durr:
            break

print(total_duration)
for ex in exercises:
    print(ex.name)"""



