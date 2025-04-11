from flask_mongoengine import MongoEngine
from datetime import datetime
from models.instructor import Instructor  # Asegúrate de importar la clase Instructor

db = MongoEngine()

class Guia(db.Document):
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    program = db.StringField(required=True)
    pdf = db.FileField(required=True)
    date_uploaded = db.DateTimeField(default=datetime.utcnow)
    instructor = db.ReferenceField(Instructor)  # Usa la clase Instructor directamente
