from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.Modelo.Objeto_Perdido import ObjetoPerdido  


objeto_bp = Blueprint('objeto', __name__)

@objeto_bp.route('/subir_objeto', methods=['GET', 'POST'])
def subir_objeto():
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        sala_encontrada = request.form.get('sala_encontrada')
        hora_encontrada = request.form.get('hora_encontrada')
        fecha_encontrada = request.form.get('fecha_encontrada')

        # Manejamos el archivo de imagen si está presente
        foto = None
        if 'foto' in request.files:
            foto = request.files['foto'].read()  # Leemos el archivo como binario
        
        # Creamos un nuevo registro de Objeto Perdido
        nuevo_objeto = ObjetoPerdido(
            nombre=nombre,
            descripcion=descripcion,
            foto=foto,
            sala_encontrada=sala_encontrada,
            hora_encontrada=hora_encontrada,
            fecha_encontrada=fecha_encontrada
        )

        db.session.add(nuevo_objeto)
        db.session.commit()

        return redirect(url_for('objeto.subir_objeto'))

    return render_template('Subir_Objeto.html')
