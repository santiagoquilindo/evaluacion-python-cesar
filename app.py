from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Message, Mail
from dotenv import load_dotenv
import os
from flask_mongoengine import MongoEngine 
from datetime import datetime 

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')


load_dotenv()


app.config['MONGODB_SETTINGS'] = {
    'db': 'guias_aprendizaje',  
    'host': os.getenv('MONGO_URI')  
}


db = MongoEngine(app)


mail = Mail(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        instructor = Instructor.objects(email=email, password=password).first()
        if instructor:
            session['instructor_id'] = str(instructor.id)
            return redirect(url_for('home'))
        else:
            return 'Credenciales inválidas'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        regional = request.form['regional']
        password = request.form['password']

        instructor = Instructor(name=name, email=email, regional=regional, password=password)
        instructor.save()

        
        msg = Message('Bienvenido al sistema', recipients=[email])
        msg.body = f'Hola {name}, tus credenciales son: {email} - {password}'
        mail.send(msg)

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/upload_guide', methods=['GET', 'POST'])
def upload_guide():
    if 'instructor_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        program = request.form['program']
        pdf = request.files['pdf']
        
        instructor = Instructor.objects(id=session['instructor_id']).first()
        file_path = os.path.join('static/guides', pdf.filename)
        pdf.save(file_path)

        guia = Guia(name=name, description=description, program=program, pdf=file_path, instructor=instructor)
        guia.save()

        return redirect(url_for('guide_list'))

    return render_template('upload_guide.html')

@app.route('/guide_list')
def guide_list():
    if 'instructor_id' not in session:
        return redirect(url_for('login'))

    guides = Guia.objects()
    return render_template('guide_list.html', guides=guides)

@app.route('/')
def home():
    if 'instructor_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')



class Instructor(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    regional = db.StringField(required=True)
    password = db.StringField(required=True)

class Guia(db.Document):
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    program = db.StringField(required=True)
    pdf = db.FileField(required=True)
    date_uploaded = db.DateTimeField(default=datetime.utcnow)  
    instructor = db.ReferenceField(Instructor)

if __name__ == '__main__':
    app.run(debug=True)

