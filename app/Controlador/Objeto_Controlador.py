import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.Modelo.Usuario import Usuario
from app.Modelo.Objeto_Perdido import ObjetoPerdido
from app.Modelo.Historial import Historial
from datetime import datetime
import pytz

chile_tz = pytz.timezone('Chile/Continental')
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

objeto_bp = Blueprint('objeto', __name__)

@objeto_bp.route('/subir_objeto', methods=['GET', 'POST'])
@login_required
def subir_objeto():
    if request.method == 'POST':
        try:
            # Datos del formulario
            nombre_objeto = request.form['nombre']
            descripcion = request.form['descripcion']
            sala_encontrada = request.form['sala_encontrada']
            hora_encontrada = request.form['hora_encontrada']
            foto = request.files['foto'] if 'foto' in request.files else None
            
            # Validar el tamaño de la foto
            if foto and len(foto.read()) > MAX_IMAGE_SIZE:
                flash('La imagen es demasiado grande. Tamaño máximo: 5 MB.', 'error')
                return redirect(url_for('objeto.subir_objeto'))

            # Reiniciar puntero del archivo
            if foto:
                foto.seek(0)  # Volver al inicio del archivo para su lectura posterior
                foto_datos = foto.read()
            else:
                foto_datos = None

            # Usuario autenticado
            usuario_actual = current_user
            rut_usuario = usuario_actual.rut

            # Crear el nuevo objeto
            nuevo_objeto = ObjetoPerdido(
                nombre_objeto=nombre_objeto,
                descripcion=descripcion,
                foto=foto_datos,
                sala_encontrada=sala_encontrada,
                hora_encontrada=hora_encontrada,
                activo=True,
                rut_usuario=rut_usuario
            )
            db.session.add(nuevo_objeto)
            db.session.commit()

            # Registrar en el historial
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
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al subir el objeto: {str(e)}', 'error')

        return redirect(url_for('objeto.subir_objeto'))

    return render_template('Subir_Objeto.html')


@objeto_bp.route('/ocultar_objeto', methods=['POST'])
@login_required
def ocultar_objeto():
    objeto_id = request.form.get('objeto_id')  # Obtener el ID del objeto desde el formulario
    rut = request.form.get('rut')  # Obtener el RUT del formulario

    if not objeto_id:
        flash('ID del objeto no proporcionado.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))

    if not rut:
        flash('RUT del usuario que retira no proporcionado.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))

    # Verificar que el objeto_id sea un número entero válido
    if not objeto_id.isdigit():
        flash('El ID del objeto debe ser un número válido.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))

    # Convertir objeto_id a entero
    objeto_id = int(objeto_id)

    # Buscar el objeto en la base de datos (ajustado al campo id_objeto)
    objeto = ObjetoPerdido.query.filter_by(id_objeto=objeto_id).first()  # Usar filter_by() con id_objeto
    if objeto is None:
        flash('No se encontró el objeto especificado.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))

    try:
        # Actualizar el estado del objeto a inactivo
        objeto.activo = False
        db.session.commit()

        # Buscar el historial relacionado con el objeto (ajustado a id_objeto)
        historial = Historial.query.filter_by(id_objeto=objeto.id_objeto).first()  # Usar id_objeto aquí
        if historial:
            # Actualizar el campo entregado_a con el RUT del usuario que retira el objeto
            historial.entregado_a = rut
            db.session.commit()

            flash('El objeto ha sido marcado como retirado y actualizado en el historial.', 'success')
        else:
            flash('No se encontró un historial asociado al objeto.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al actualizar el historial: {str(e)}', 'error')

    return redirect(url_for('listara.lista_objetos_admin'))



