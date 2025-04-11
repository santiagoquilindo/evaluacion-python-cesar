from flask_mongoengine import MongoEngine

db = MongoEngine()

class Instructor(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    regional = db.StringField(required=True)
    password = db.StringField(required=True)
