from flask import Flask, request
from flask_api import FlaskAPI

from server.database import Database, Note
import json 
from server.schema import SchemaValidator

app = FlaskAPI("myserver")
db = Database('db.sqlite3')
validator = SchemaValidator()


@app.route('/notes', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.json

        errors = validator.compare(Note, data)
        if errors:
            return errors

        db.write(data)
        return data
    else:
        alldata = db.all()
        return alldata


@app.route('/notes/<name>/tags')
def note_tags(note_name):
    note = db.get(note_name)
    if note is not None:
        return note.tags


@app.route('/tags/<name>/notes/')
def notes_by_tag(name: str):
    return []
    
