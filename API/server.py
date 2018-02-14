from flask import Flask, render_template, Response, request
import json
import sqlite3
from Scripts.log import Log, LogFromFile

app = Flask(__name__)
app.config['DEBUG'] = False

#database connections - path to data.db on server /Project/Music-Driven-Workout-App/data.db
conn = sqlite3.connect("/Project/Music-Driven-Workout-App/data.db", isolation_level=None)
c = conn.cursor()

#documentation page
@app.route('/')
def index():
	return render_template('index.html')

#sample route for how api routing works
@app.route('/api')
def api():
	return Response(json.dumps({"Message": "Welcome to the API", "Status" : "Success"}), mimetype='application/json')

@app.route('/api/database/', methods=['POST'])
def database():
	query = request.form.get('query')
	key = request.form.get('key')
	if (query == None or key == None):
		return failure("Invalid parameters")
	if (key != "SoftCon2018"):
		return failure("Invalid authentication")
	try:
		c.execute(query)
	except Exception as e:
		return failure(str(e))
	result = c.fetchall()
	return Response(json.dumps({"Query": query, "Result": result, "Status": "Success"}), mimetype='application/json')

#Workouts test 1


#Fitness test 1
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
	except Exception as e:
		return failure(str(e))
	return standardRes(log1.getFrequency())

#api messages
def failure(msg):
	return Response(json.dumps({"Status": "Failure - " + msg}), mimetype='application/json')
def standardRes(data):
	return Response(json.dumps({"Result": data, "Status": "Success"}), mimetype='application/json')
