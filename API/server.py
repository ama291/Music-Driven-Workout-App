from flask import Flask, render_template, Response, request
import json
import sqlite3
app = Flask(__name__)
app.config['DEBUG'] = False

#database connections - path to data.db on server /Project/Music-Driven-Workout-App/data.db
conn = sqlite3.connect("/Project/Music-Driven-Workout-App/data.db")
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

#fail messages
def failure(msg):
	return Response(json.dumps({"Status": "Failure - " + msg}), mimetype='application/json')