from flask import Flask, render_template, Response, request
import json
import sqlite3
from Scripts.log import Log, LogFromFile
from Scripts.driver import *

app = Flask(__name__)
app.config['DEBUG'] = False

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
	return standardRes("Welcome to the API");

@app.route('/api/database/', methods=['POST'])
def queryDatabase():
	query = request.form.get('query')
	key = request.form.get('key')
	if (query == None or key == None):
		return failure("Invalid parameters")
	if (key != "SoftCon2018"):
		return failure("Invalid authentication")
	try:
		c.execute(query)
		result = c.fetchall()
		return standardRes(result)
	except Exception as e:
		return failure(str(e))
#TODO
@app.route('/api/fitness/tracked/', methods=['POST'])
def getTracked():
	userid = request.form.get('userid')
	key = request.form.get('key')
	if (userid == None or key == None):
		return failure("Invalid parameters")
	if (key != "SoftCon2018"):
		return failure("Invalid authentication")
	try:
		return failure("Route not configured")
		#return standardRes(getTrackedExercises(userid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/fitness/istracked/', methods=['POST'])
def checkTracked():
	userid = request.form.get('userid')
	exid = request.form.get('exid')
	key = request.form.get('key')
	if (userid == None or exid == None or key == None):
		return failure("Invalid parameters")
	if (key != "SoftCon2018"):
		return failure("Invalid authentication")
	try:
		return failure("Route not configured")
		#return standardRes(isTracked(userid, exid))
	except Exception as e:
		return failure(str(e))

#TODO
@app.route('/api/fitness/test/', methods=['POST'])
def getFitness():
	userid = request.form.get('userid')
	categories = request.form.get('categories')
	numExercises = request.form.get('numExercises')
	key = request.form.get('key')
	if (userid == None or categories == None or numExercises == None or key == None):
		return failure("Invalid parameters")
	if (key != "SoftCon2018"):
		return failure("Invalid authentication")
	try:
		return failure("Route not configured") 
		#return standardRes(getFitnessTest(categories, numExercises, getTrackedExercises(userid))
	except Exception as e:
		return failure(str(e))

@app.route('/api/fitness/accel/', methods=['POST'])
def accel():
	data = request.form.get('data')
	key = request.form.get('key')
	if (data == None or key == None):
		return failure("Invalid parameters")
	if (key != "SoftCon2018"):
		return failure("Invalid authentication")
	try:
		log1 = Log(json.loads(data))
		return standardRes(log1.getFrequency())
	except Exception as e:
		return failure(str(e))

#api messages
def failure(msg):
	return Response(json.dumps({"Status": "Failure - " + msg}), mimetype='application/json')
def standardRes(data):
	return Response(json.dumps({"Result": data, "Status": "Success"}), mimetype='application/json')