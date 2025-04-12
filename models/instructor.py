from flask_mongoengine import MongoEngine
from mongoengine import StringField, ReferenceField, Document
from models.regional import Sena

db = MongoEngine()

class Instructor(Document):
    nombrecompleto = StringField(required=True)
    correoelectronico = StringField(required=True, unique=True)
    regional = ReferenceField(Sena, required=True)

    def __str__(self):
        return self.nombrecompleto
