from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.Modelo.Objeto_Perdido import ObjetoPerdido
from app.Modelo.Historial import Historial
from datetime import datetime
import pytz

chile_tz = pytz.timezone('Chile/Continental')

objeto_bp = Blueprint('objeto', __name__)

@objeto_bp.route('/subir_objeto', methods=['GET', 'POST'])
@login_required
def subir_objeto():
    if request.method == 'POST':
        nombre_objeto = request.form['nombre']  # Cambié 'nombre' por 'nombre_objeto'
        descripcion = request.form['descripcion']
        foto = request.files['foto'].read()  # Asegúrate de que 'foto' es opcional si no siempre se sube
        sala_encontrada = request.form['sala_encontrada']
        hora_encontrada = request.form['hora_encontrada']

        # Usuario autenticado
        usuario_actual = current_user  # current_user viene de flask-login
        rut_usuario = usuario_actual.rut  # Supongo que el usuario tiene un campo 'rut'

        # Crear el nuevo objeto
        nuevo_objeto = ObjetoPerdido(
            nombre_objeto=nombre_objeto,  # Asegúrate de que coincida con el nombre en la clase ObjetoPerdido
            descripcion=descripcion,
            foto=foto,
            sala_encontrada=sala_encontrada,
            hora_encontrada=hora_encontrada,
            activo=True,
            rut_usuario=rut_usuario  # Aquí pasamos el rut del usuario
        )

        # Guardar en la base de datos
        db.session.add(nuevo_objeto)
        db.session.commit()

        # Agregar entrada al historial
        nueva_historial = Historial(
            id_objeto=nuevo_objeto.id_objeto,
            rut_usuario=rut_usuario,
            sala_encontrada=sala_encontrada,
            descripcion=descripcion,
            activo=nuevo_objeto.activo
        )
        db.session.add(nueva_historial)
        db.session.commit()

        flash('Objeto subido correctamente y registrado en el historial.', 'success')
        return redirect(url_for('objeto.subir_objeto'))

    return render_template('Subir_Objeto.html')


@objeto_bp.route('/ocultar_objeto', methods=['POST'])
@login_required
def ocultar_objeto():
    objeto_id = request.form.get('objeto_id')
    retirado_por = request.form.get('retirado_por')

    if not objeto_id:
        flash('ID del objeto no proporcionado.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))

    # Buscar el objeto en la base de datos
    objeto = ObjetoPerdido.query.get(objeto_id)
    if objeto:
        # Actualizar el estado del objeto y registrar en el historial
        objeto.activo = False
        db.session.commit()

        # Registrar en el historial quién retiró el objeto
        nueva_historial = Historial(
            id_objeto=objeto.id_objeto,
            accion=f"Retirado por {retirado_por}",
            fecha=datetime.now(chile_tz),
            activo=objeto.activo
        )
        db.session.add(nueva_historial)
        db.session.commit()

        flash('El objeto ha sido marcado como retirado y registrado en el historial.', 'success')
    else:
        flash('No se encontró el objeto especificado.', 'error')

    return redirect(url_for('listara.lista_objetos_admin'))
