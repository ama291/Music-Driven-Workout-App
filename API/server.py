from flask import Flask, render_template, Response
import json
import sqlite3
app = Flask(__name__)
app.config['DEBUG'] = False

#database connections - path to data.db on server
conn = sqlite3.connect("/Project/Music-Driven-Workout-App/data.db")
c = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    return Response(json.dumps({"Message": "Welcome to the API", "Status" : "Success"}), mimetype='application/json')

@app.route('/api/database/<string:query>')
def database(query):
    return Response(json.dumps({"Query": query, "Status": "Success"}), mimetype='application/json')