from flask import Flask
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


@app.route("/list", methods=['GET'])
def getTodoList():
    q = request.args.get('q', False)
    db = create_engine(db_string)
    db.execute("CREATE TABLE IF NOT EXISTS notes (title text)")  
    result_set = db.execute("SELECT * FROM notes")  
    notes = [r['title'] for r in result_set if q.lower() in r['title'].lower()]
    return jsonify(notes)

@app.route("/add", methods=['POST'])
def addTodo():
    text = request.get_json().get('text', False)
    if text and len(text) >= 10 and len(text) <= 100:
        db = create_engine(db_string)
        db.execute("CREATE TABLE IF NOT EXISTS notes (title text)")  
        db.execute("INSERT INTO notes (title) VALUES ('" + text + "')")
        return jsonify({'success': True})
    else: # else ignore if text is to long, to short or no text is provided
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run()