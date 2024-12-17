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

            nombre_objeto = request.form['nombre']
            descripcion = request.form['descripcion']
            sala_encontrada = request.form['sala_encontrada']
            hora_encontrada = request.form['hora_encontrada']
            foto = request.files['foto'] if 'foto' in request.files else None

            if foto and len(foto.read()) > MAX_IMAGE_SIZE:
                flash('La imagen es demasiado grande. Tamaño máximo: 5 MB.', 'error')
                return redirect(url_for('objeto.subir_objeto'))

            if foto:
                foto.seek(0) 
                foto_datos = foto.read()
            else:
                foto_datos = None


            usuario_actual = current_user
            rut_usuario = usuario_actual.rut

           
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




