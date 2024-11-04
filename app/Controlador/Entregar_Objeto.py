from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.Modelo import Objeto_Perdido, Historial

entregar_bp = Blueprint('entregar', __name__)

@entregar_bp.route('/entregar_objeto', methods=['POST'])
@login_required
def entregar_objeto():
    # Obtén el ID del objeto del formulario
    objeto_id = request.form.get('id')

    # Verifica si el ID es válido
    if objeto_id is None:
        flash('ID de objeto no proporcionado', 'error')
        return redirect(url_for('objeto.lista_objetos_admin'))  # Redirigir a la lista de objetos

    # Busca el objeto en la base de datos
    objeto = Objeto_Perdido.query.get(objeto_id)

    if objeto is None:
        flash('Objeto no encontrado', 'error')
        return redirect(url_for('objeto.lista_objetos_admin'))  # Redirigir a la lista de objetos

    # Crea una entrada en el historial para registrar la entrega
    historial = Historial(objeto_id=objeto.id, usuario_id=current_user.id)
    db.session.add(historial)

    # Marca el objeto como entregado (opcional)
    objeto.activo = False  # Si deseas que el objeto ya no esté disponible
    db.session.commit()

    flash('Objeto entregado exitosamente', 'success')
    return redirect(url_for('objeto.lista_objetos_admin'))  # Redirigir a la lista de objetos
