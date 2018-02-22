from flask import Flask, render_template, Response
import json
app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    return Response(json.dumps({"Status": "Welcome to the API."}), mimetype='application/json')

@app.route('/api/goals/addgoal/', methods=["POST"])
def apiAddGoal():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	goalName = request.form.get('goalname')
	goalDescription = request.form.get('goaldescription')
	goalNum = int(request.form.get('goalnum'))
	categories = request.form.get('categories')
	if (categories != None):
		categories = categories.split(",")
	muscleGroups = request.form.get('musclegroups')
	if (muscleGroups != None):
		muscleGroups = muscleGroups.split(",")
	duration = int(request.form.get('duration'))
	daysPerWeek = int(request.form.get('daysperweek'))
	key = request.form.get('key')

	params = [userid, goalName, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = addGoal(userid, goalDescription, goalNum, categories, muscleGroups, duration, daysPerWeek, notify)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))

@app.route('/api/goals/removegoal/', methods=["POST"])
def apiRemoveGoal():
	userid = request.form.get('userid')
	if (userid != None):
		userid = int(userid)
	goalName = request.form.get('goalname')
	goalDescription = request.form.get('goaldescription')
	goalNum = int(request.form.get('goalnum'))
	categories = request.form.get('categories')
	if (categories != None):
		categories = categories.split(",")
	muscleGroups = request.form.get('musclegroups')
	if (muscleGroups != None):
		muscleGroups = muscleGroups.split(",")
	duration = int(request.form.get('duration'))
	daysPerWeek = int(request.form.get('daysperweek'))
	key = request.form.get('key')

	params = [userid, goalName, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = removeGoal(userid, goalDescription, goalNum, categories, muscleGroups, duration, daysPerWeek, notify)
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
	numWorkouts = int(request.form.get('numworkouts'))
	key = request.form.get('key')

	params = [userid, key]
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
	theme = request.form.get('theme')
	numWorkouts = int(request.form.get('numworkouts'))
	key = request.form.get('key')

	params = [userid, key]
	if (None in params):
		return failure("Invalid parameters")
	if (key != masterKey):
		return failure("Invalid authentication")
	try:
		response = removeTheme(userid, themeName, theme, numWorkouts)
		return standardRes(json.dumps(response))
	except Exception as e:
		return failure(str(e))
