from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_required
from datetime import datetime
from app import db
from app.Modelo.Objeto_Perdido import ObjetoPerdido
from app.Modelo.Historial import Historial
import pytz

chile_tz = pytz.timezone('Chile/Continental')

entregar_bp = Blueprint('entregar', __name__)

@entregar_bp.route('/entregar_objeto', methods=['POST'])
@login_required
def entregar_objeto():
    objeto_id = request.form.get('objeto_id')  # ID del objeto desde el formulario
    retirado_por = request.form.get('retirado_por')  # Nombre de quien retira
    rut = request.form.get('rut')  # RUT del usuario que retira

    # Validar que se hayan proporcionado los datos necesarios
    if not objeto_id or not objeto_id.isdigit():
        flash('ID del objeto no proporcionado o inválido.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))

    if not rut:
        flash('RUT del usuario que retira no proporcionado.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))

    # Convertir objeto_id a entero
    objeto_id = int(objeto_id)

    # Buscar el objeto en la base de datos
    objeto = ObjetoPerdido.query.filter_by(id_objeto=objeto_id).first()
    if not objeto:
        flash('No se encontró el objeto especificado.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))

    try:
        # Actualizar el estado del objeto a inactivo
        objeto.activo = False
        db.session.commit()

        print(f"Objeto actualizado: id={objeto.id_objeto}, activo={objeto.activo}")

        # Buscar el historial del objeto (si existe)
        historial = Historial.query.filter_by(id_objeto=objeto_id, activo=True).first()
        
        if historial:
            # Si existe un historial activo, actualizamos su estado
            historial.accion = {retirado_por}
            historial.fecha_accion = datetime.now(chile_tz)
            historial.activo = False  # Marcar como inactivo el historial
            historial.entregado_a = rut
            db.session.commit()

            print(f"Historial actualizado: id_objeto={historial.id_objeto}, entregado_a={historial.entregado_a}")
        else:
            # Si no existe historial, crear uno nuevo
            nueva_historial = Historial(
                id_objeto=objeto.id_objeto,
                accion=f"Retirado por {retirado_por}",
                fecha=datetime.now(chile_tz),
                activo=False,
                entregado_a=rut
            )
            db.session.add(nueva_historial)
            db.session.commit()

            print(f"Historial creado: id_objeto={nueva_historial.id_objeto}, entregado_a={nueva_historial.entregado_a}")

        flash('El objeto ha sido marcado como retirado y registrado en el historial.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error al insertar o actualizar historial: {e}")
        flash(f'Ocurrió un error al actualizar el historial: {e}', 'error')

    return redirect(url_for('listara.lista_objetos_admin'))
