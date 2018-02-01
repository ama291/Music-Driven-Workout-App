from flask import Flask, render_template
import json
app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    return json.dumps({"Status": "Welcome to the API."})