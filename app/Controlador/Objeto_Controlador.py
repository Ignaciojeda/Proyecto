from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.Modelo.Objeto_Perdido import ObjetoPerdido  


objeto_bp = Blueprint('objeto', __name__)

@objeto_bp.route('/subir_objeto', methods=['GET', 'POST'])
def subir_objeto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        foto = request.files['foto'].read()  # Lee el archivo como binario
        sala_encontrada = request.form['sala_encontrada']
        hora_encontrada = request.form['hora_encontrada']
        fecha_encontrada = request.form['fecha_encontrada']

        nuevo_objeto = ObjetoPerdido(
            nombre=nombre,
            descripcion=descripcion,
            foto=foto,
            sala_encontrada=sala_encontrada,
            hora_encontrada=hora_encontrada,
            fecha_encontrada=fecha_encontrada
        )

        # Guardar en la base de datos
        db.session.add(nuevo_objeto)
        db.session.commit()
        
        return redirect(url_for('objeto.subir_objeto'))

    return render_template('Subir_Objeto.html')
