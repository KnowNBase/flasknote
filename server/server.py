from flask import Flask  # type: ignore

from server.adapters.create_note import create_note_chain
from server.adapters.list_notes import list_notes_chain
from server.generator import Generator

app = Flask(__name__)
generator = Generator(app)
generator([create_note_chain, list_notes_chain])
