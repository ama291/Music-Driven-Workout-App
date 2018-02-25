from flask import Flask, render_template, Response, request
import json
import sqlite3
from Scripts.log import Log
from Scripts.driver import *
from Scripts.fitnessTest import *
from CLI.apiCalls import toBool
from Scripts.dbfunctions import getAllFromColumn, realDB

dbURL = realDB

app = Flask(__name__)
app.config['DEBUG'] = False
masterKey = "SoftCon2018"

#documentation page
@app.route('/')
def index():
	return render_template('index.html')

#sample route for how api routing works
@app.route('/api')
def getApi():
	return standardRes("Welcome to the API")

@app.route('/api/getusername/', methods=['POST'])
def apiGetUsername():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	key = request.form.get('key')
	params = [userid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = requests.post('http://138.197.49.155:5000/api/database/', data = {'query': 'SELECT spotifyUsername FROM users where id=' + str(userid), 'key': key})
		return standardRes(response.json()['Result'][0][0])
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/getuserid/', methods=['POST'])
def apiGetUserId():
	username = request.form.get('username')
	key = request.form.get('key')
	params = [username, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = getUserId(username)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/onboarding/', methods=['POST'])
def apiOnboarding():
	username = request.form.get('username')
	height = request.form.get('height')
	if (height != None):
		height = int(height)
	weight = request.form.get('weight')
	if (weight != None):
		weight = int(weight)
	year = request.form.get('year')
	if (year != None):
		year = int(year)
	key = request.form.get('key')
	params = [username, height, weight, year, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = onboarding(username, height, weight, year)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/getworkout/', methods=['POST'])
def apiGetWorkout():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	equipment = request.form.get('equipment')
	if (equipment != None):
		equipment = equipment.split(",")
	else:
		equipment = []
	duration = request.form.get('duration')
	if (duration != None):
		duration = int(duration)
	difficulty = request.form.get('difficulty')
	accessToken = request.form.get('token')
	cats = request.form.get('categories')
	if (cats != None):
		cats = cats.split(",")
	groups = request.form.get('musclegroups')
	if (groups != None):
		groups = groups.split(",")
	themes = request.form.get('themes')
	if (themes != None):
		themes = equipment.split(",")
	key = request.form.get('key')
	params = [userid, duration, difficulty, accessToken, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = getWorkout(userid, themes, cats, groups, equipment, duration, difficulty, accessToken)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/startworkout/', methods=['POST'])
def apiStartWorkout():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	workout = request.form.get('workout')
	key = request.form.get('key')
	params = [userid, workout, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = startWorkout(userid, workout)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/pauseworkout/', methods=['POST'])
def apiPauseWorkout():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	workoutid = request.form.get('workoutid')
	pausedOn = request.form.get('paused')
	if (pausedOn != None):
		pausedOn = int(pausedOn)
	key = request.form.get('key')
	params = [userid, workoutid, pausedOn, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = pauseWorkout(userid, workoutid, pausedOn)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/quitworkout/', methods=['POST'])
def apiQuitWorkout():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	workoutid = request.form.get('workoutid')
	key = request.form.get('key')
	params = [userid, workoutid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = quitWorkout(userid, workoutid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/saveworkout/', methods=['POST'])
def apiSaveWorkout():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	workoutid = request.form.get('workoutid')
	key = request.form.get('key')
	params = [userid, workoutid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = saveWorkout(userid, workoutid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/unsaveworkout/', methods=['POST'])
def apiUnSaveWorkout():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	workoutid = request.form.get('workoutid')
	key = request.form.get('key')
	params = [userid, workoutid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = unsaveWorkout(userid, workoutid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/startsavedworkout/', methods=['POST'])
def apiStartSavedWorkout():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	workoutid = request.form.get('workoutid')
	key = request.form.get('key')
	params = [userid, workoutid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = startSavedWorkout(userid, workoutid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/workoutssaved/', methods=['POST'])
def apiWorkoutsSaved():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	key = request.form.get('key')
	params = [userid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = workoutsSaved(userid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/workouts/workoutsinprogress/', methods=['POST'])
def apiWorkoutsInProgress():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	if (userid != None):
		userid = int(userid)
	key = request.form.get('key')
	params = [userid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = workoutsInProgress(userid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))


@app.route('/api/fitness/accel/', methods=['POST'])
def accel():
	data = request.form.get('data')
	key = request.form.get('key')
	params = [data, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		log1 = Log(json.loads(data), data=True)
		return standardRes(log1.getFrequency())
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitness/addexact/', methods=['POST'])
def apiAddExerciseExact():
	userID = request.form.get('userid')
	if userID != None:
		userID = int(userID)
	exID = request.form.get('exid')
	if exID != None:
		exID = int(exID)
	timestamp = request.form.get('timestamp')
	rate = request.form.get('rate')
	if rate != None:
		rate = float(rate)
	key = request.form.get('key')
	params = [userID, exID, timestamp, rate, key]
	if None in params:
		return failure("Invalid parameters")
	if key != masterKey:
		return failure("Invalid authentication")
	try:
		response = addExerciseExact(userID, exID, timestamp, rate)
		return standardRes(str(response))
	except Exception as e:
		return failure(str(e))


@app.route('/api/fitness/tracked/', methods=['POST'])
def apiGetTracked():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	categories = request.form.get('categories')
	if (categories != None):
		categories = categories.split(",")
	key = request.form.get('key')
	params = [userid, categories, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = getTrackedExercises(userid, categories=categories)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitness/test/', methods=['POST'])
def apiGetFitness():
	categories = request.form.get('categories')
	if (categories != None):
		categories = categories.split(",")
	numexercises = int(request.form.get('numexercises'))
	exerciseids = request.form.get('exerciseids')
	if (exerciseids != None):
		exerciseids = exerciseids.split(",")
		temp = exerciseids
		exerciseids = list(map(int, temp))
	key = request.form.get('key')
	params = [categories, numexercises, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = getFitnessTest(categories, numexercises, exerciseids)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitness/istracked/', methods=['POST'])
def apiIsTracked():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	exid = request.form.get('exid')
	key = request.form.get('key')
	params = [userid, exid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = isTracked(userid, exid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/fitness/toggletracked/', methods=['POST'])
def apiToggleTracked():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	exid = int(request.form.get('exid'))
	key = request.form.get('key')
	params = [userid, exid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = toggleTracked(userid, exid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitness/getexercise/', methods=['POST'])
def apiGetExercise():
	exid = request.form.get('exid')
	if (exid != None):
		exid = int(exid)
	key = request.form.get('key')
	params = [exid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = getExerciseFromID(exid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitenss/getuserexercises/', methods=['POST'])
def apiGetUserExercises():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	key = request.form.get('key')
	params = [userid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = getUserExercises(userid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitness/getprevious/', methods=["POST"])
def apiGetPrevious():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	exid = request.form.get('exid')
	key = request.form.get('key')
	params = [userid, exid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = getPreviousResults(userid, exid)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitness/getexsbytype/', methods=["POST"])
def apiGetExercisesByType():
	category = request.form.get('category')
	muscleGroup = request.form.get('muscle')
	equipment = request.form.get('equipment')
	key = request.form.get('key')
	params = [category, muscleGroup, equipment, key]
	if None in params:
		return failure("Invalid parameters")
	if key != masterKey:
		return failure("Invalid authentication")
	try:
		response = getExercisesbyType(category, muscleGroup, equipment)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitness/getcategories/', methods=["POST"])
def apiGetCategories():
	key = request.form.get('key')
	if key != masterKey:
		return failure("Invalid authentication")
	try:
		response = getAllFromColumn(dbURL, "exercises", "type")
		return standardRes(json.dumps(response))
	except:
		return failure(str(e))


@app.route('/api/fitness/getmuscles/', methods=["POST"])
def apiGetMuscles():
	key = request.form.get('key')
	if key != masterKey:
		return failure("Invalid authentication")
	try:
		response = getAllFromColumn(dbURL, "exercises", "muscle")
		return standardRes(json.dumps(response))
	except:
		return failure(str(e))


@app.route('/api/fitness/getequipments/', methods=["POST"])
def apiGetEquipments():
	key = request.form.get('key')
	if key != masterKey:
		return failure("Invalid authentication")
	try:
		response = getAllFromColumn(dbURL, "exercises", "equipment")
		return standardRes(json.dumps(response))
	except:
		return failure(str(e))




@app.route('/api/goals/addgoal/', methods=["POST"])
def apiAddGoal():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	name = request.form.get('name')
	description = request.form.get('description')
	goalNum = request.form.get('goalnum')
	if goalNum != None:
		goalNum = int(goalNum)
	categories = request.form.get('categories')
	if categories != None:
		categories = categories.split(",")
	muscleGroups = request.form.get('musclegroups')
	if muscleGroups != None:
		muscleGroups = muscleGroups.split(",")
	duration = request.form.get('duration')
	if duration != None:
		duration = int(duration)
	daysPerWeek = request.form.get('daysperweek')
	if daysPerWeek != None:
		daysPerWeek = int(daysPerWeek)
	notify = request.form.get('notify')
	if notify != None:
		notify = toBool(notify)
	key = request.form.get('key')
	params = [userid, name, description, goalNum, categories, \
	 muscleGroups, duration, daysPerWeek, notify, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = addGoal(userid, name, description, goalNum, \
		 categories, muscleGroups, duration, daysPerWeek, notify)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/goals/removegoal/', methods=["POST"])
def apiRemoveGoal():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	name = request.form.get('name')
	key = request.form.get('key')
	params = [userid, name, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = removeGoal(userid, name)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/themes/addtheme/', methods=["POST"])
def apiAddTheme():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	themeName = request.form.get('themename')
	theme = request.form.get('theme')
	numWorkouts = request.form.get('numworkouts')
	if numWorkouts != None:
		numWorkouts = int(numWorkouts)
	key = request.form.get('key')
	params = [userid, themeName, theme, numWorkouts, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = addTheme(userid, themeName, theme, numWorkouts)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/themes/removetheme/', methods=["POST"])
def apiRemoveTheme():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	themeName = request.form.get('themename')
	key = request.form.get('key')
	params = [userid, themeName, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = removeTheme(userid, themeName)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

#api messages
def failure(msg):
	return Response(json.dumps({"Status": "Failure - " + msg}), mimetype='application/json')
def standardRes(data):
	return Response(json.dumps({"Result": data, "Status": "Success"}), mimetype='application/json')
