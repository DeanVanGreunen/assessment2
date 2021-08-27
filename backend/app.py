from flask import Flask, request, jsonify, make_response
from flask import jsonify
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

db = SQLAlchemy(app)
db_string = "postgresql://postgres:postgres@localhost:5432/postgres"


@app.route("/list", methods=['GET', 'OPTIONS'])
def getTodoList():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    q = request.args.get('q', False)
    db = create_engine(db_string)
    db.execute("CREATE TABLE IF NOT EXISTS notes (title text)")  
    result_set = db.execute("SELECT * FROM notes")  
    notes = [r['title'] for r in result_set if q.lower() in r['title'].lower()]
    return _corsify_actual_response(jsonify(notes))

@app.route("/add", methods=['POST', 'OPTIONS'])
def addTodo():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    text = request.get_json().get('text', False)
    if text and len(text) >= 10 and len(text) <= 100:
        db = create_engine(db_string)
        db.execute("CREATE TABLE IF NOT EXISTS notes (title text)")  
        db.execute("INSERT INTO notes (title) VALUES ('" + text + "')")
        return _corsify_actual_response(jsonify({'success': True}))
    else: # else ignore if text is to long, to short or no text is provided
        return _corsify_actual_response(jsonify({'success': False}))

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')