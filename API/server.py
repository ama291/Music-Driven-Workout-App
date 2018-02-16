from flask import Flask, render_template, Response, request
import json
import sqlite3
from Scripts.log import Log
from Scripts.driver import *
from Scripts.fitnessTest import *

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
	duration = int(request.form.get('duration'))
	difficulty = request.form.get('difficulty')
	cats = request.form.get('categories')
	if (cats != None):
		cats = cats.split(",")
	groups = request.form.get('musclegroups')
	if (groups != None):
		groups = groups.split(",")
	thems = request.form.get('themes')
	if (thems != None):
		thems = equipment.split(",")
	key = request.form.get('key')
	params = [userid, duration, difficulty, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = getWorkout(userid, equipment, duration, difficulty, categories = cats, muscleGroups = groups, themes = thems)
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
	key = request.form.get('key')
	params = [userid, workoutid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = pauseWorkout(userid, workoutid, 0)
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
def apiStartSaveWorkout():
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
		response = workoutsinprogress(userid)
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

@app.route('/api/fitness/tracked/', methods=['POST'])
def apiGetTracked():
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
		response = getTrackedExercises(userid)
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
def apiCheckTracked():
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
		return failure("Route not configured")
		response =toggleTracked(userid, exid)
	except Exception as e:
		return failure(str(e))

#api messages
def failure(msg):
	return Response(json.dumps({"Status": "Failure - " + msg}), mimetype='application/json')
def standardRes(data):
	return Response(json.dumps({"Result": data, "Status": "Success"}), mimetype='application/json')
