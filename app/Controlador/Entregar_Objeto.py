from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.Modelo import Historial
from app.Modelo.Objeto_Perdido import ObjetoPerdido

entregar_bp = Blueprint('entregar', __name__)

@entregar_bp.route('/entregar_objeto', methods=['POST'])
@login_required
def entregar_objeto():
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
            historial.activo = 0
            db.session.commit()

            flash('El objeto ha sido marcado como retirado y actualizado en el historial.', 'success')
        else:
            flash('No se encontró un historial asociado al objeto.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al actualizar el historial: {str(e)}', 'error')

    return redirect(url_for('listara.lista_objetos_admin'))

