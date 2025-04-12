from flask import request, render_template, jsonify, redirect, url_for, session, flash
from models.instructor import Instructor
from models.regional import Sena
from app import app  

@app.route("/agregarintructor/", methods=['GET', 'POST'])
def addInstructor():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos = request.get_json()
            print("Datos recibidos:", datos)
            sena_id = datos.get('sena_id')
            print("Sena ID recibido:", sena_id)
            if not sena_id:
                raise ValueError("No se recibió el 'sena_id'.")
            sena = Sena.objects(id=sena_id).first()
            print("Sena encontrado:", sena)
            if not sena:
                raise ValueError("El Sena seleccionado no existe.")
            datos['regional'] = sena 
            datos['correoelectronico'] = datos.get('email') 
            del datos['email']
            del datos['sena_id'] 
            instructor = Instructor(**datos)
            instructor.save()
            estado = True
            mensaje = "Instructor agregado correctamente"
        else:
            mensaje = "Método no permitido"
    except Exception as error:
        print("Error al agregar instructor:", error)
        mensaje = str(error)
    senas = Sena.objects()
    return render_template('agregar_instructor.html', estado=estado, mensaje=mensaje, senas=senas)
