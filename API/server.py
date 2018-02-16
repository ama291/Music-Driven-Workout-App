from flask import Flask, render_template, Response, request
import json
import sqlite3
from Scripts.log import Log
from Scripts.driver import *
from Scripts.fitnessTest import *

app = Flask(__name__)
app.config['DEBUG'] = False
masterKey = "SoftCon2018"

#database connections - path to data.db on server /Project/Music-Driven-Workout-App/data.db
try:
	conn = sqlite3.connect("/Project/Music-Driven-Workout-App/data.db", isolation_level=None)
	c = conn.cursor()
except:
	print("Local testing detected - no database")

#documentation page
@app.route('/')
def index():
	return render_template('index.html')

#sample route for how api routing works
@app.route('/api')
def getApi():
	return standardRes("Welcome to the API")

#TODO
@app.route('/api/workouts/getworkout/', methods=['POST'])
def apiGetWorkout():
	userid = request.form.get('userid')
	equipment = request.form.get('equipment')
	duration = request.form.get('duration')
	difficulty = request.form.get('difficulty')
	cats = request.form.get('categories')
	groups = request.form.get('musclegroups')
	thems = request.form.get('themes')
	key = request.form.get('key')
	listparams = [equipment, cats, groups, thems]
	try:
		for l in listparams:
			if (l != None):
				l = l.split(",")
	except:
		return failure("Invalid parameters")
	params = [userid, equipment, duration, difficulty, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return standardRes(getWorkout(userid, equipment, duration, difficulty, categories = cats, muscleGroups = groups, themes = thems))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/workouts/startworkout/', methods=['POST'])
def apiStartWorkout():
	userid = request.form.get('userid')
	workout = request.form.get('workout')
	key = request.form.get('key')
	params = [userid, workout, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return standardRes(startWorkout(userid, workout))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/workouts/pauseworkout/', methods=['POST'])
def apiPauseWorkout():
	userid = request.form.get('userid')
	workoutid = request.form.get('workoutid')
	key = request.form.get('key')
	params = [userid, workoutid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return standardRes(pauseWorkout(userid, workoutid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/workouts/quitworkout/', methods=['POST'])
def apiQuitWorkout():
	userid = request.form.get('userid')
	workoutid = request.form.get('workoutid')
	key = request.form.get('key')
	params = [userid, workoutid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return standardRes(quitWorkout(userid, workoutid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/workouts/saveworkout/', methods=['POST'])
def apiSaveWorkout():
	userid = request.form.get('userid')
	workoutid = request.form.get('workoutid')
	key = request.form.get('key')
	params = [userid, workoutid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return standardRes(saveWorkout(userid, workoutid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/workouts/workoutssaved/', methods=['POST'])
def apiWorkoutsSaved():
	userid = request.form.get('userid')
	key = request.form.get('key')
	params = [userid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return standardRes(workoutsSaved(userid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/workouts/workoutsinprogress/', methods=['POST'])
def apiWorkoutsInProgress():
	userid = request.form.get('userid')
	key = request.form.get('key')
	params = [userid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return standardRes(workoutsInProgress(userid))
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
		log1 = Log(json.loads(data))
		return standardRes(log1.getFrequency())
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/fitness/tracked/', methods=['POST'])
def apiGetTracked():
	userid = request.form.get('userid')
	key = request.form.get('key')
	params = [userid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return failure("Route not configured")
		#return standardRes(getTrackedExercises(userid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/fitness/test/', methods=['POST'])
def apiGetFitness():
	userid = request.form.get('userid')
	categories = request.form.get('categories')
	numexercises = request.form.get('numexercises')
	key = request.form.get('key')
	params = [userid, categories, numexercises, key]
	if (None in params):		
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return failure("Route not configured") 
		#return standardRes(getFitnessTest(categories, numExercises, getTrackedExercises(userid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/fitness/istracked/', methods=['POST'])
def apiIsTracked():
	userid = request.form.get('userid')
	exid = request.form.get('exid')
	key = request.form.get('key')
	params = [userid, exid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return failure("Route not configured")
		#return standardRes(isTracked(userid, exid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/fitness/toggletracked/', methods=['POST'])
def apiCheckTracked():
	userid = request.form.get('userid')
	exid = request.form.get('exid')
	key = request.form.get('key')
	params = [userid, exid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		return failure("Route not configured")
		#return standardRes(toggleTracked(userid, exid))
	except Exception as e:
		return failure(str(e))

@app.route('/api/database/', methods=['POST'])
def queryDatabase():
	query = request.form.get('query')
	key = request.form.get('key')
	params = [query, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		c.execute(query)
		result = c.fetchall()
		return standardRes(result)
	except Exception as e:
		return failure(str(e))

#api messages
def failure(msg):
	return Response(json.dumps({"Status": "Failure - " + msg}), mimetype='application/json')
def standardRes(data):
	return Response(json.dumps({"Result": data, "Status": "Success"}), mimetype='application/json')