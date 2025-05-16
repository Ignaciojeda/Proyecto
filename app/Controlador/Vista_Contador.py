from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.Modelo.Pedido import Pedido
from datetime import datetime

contador_bp = Blueprint('contador', __name__)

@contador_bp.route('/')
@login_required
def dashboard():
    if current_user.tipoUsuario != 4:  
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('home.home'))

    try:
        pedidos = db.session.query(Pedido)\
            .filter_by(etapaId=4)\
            .order_by(Pedido.fechaPedido.desc())\
            .all()

        return render_template(
            'vista_contador.html',
            pedidos=pedidos,
            current_time=datetime.now()
        )
    except Exception as e:
        flash(f'Error al cargar pedidos: {str(e)}', 'error')
        return redirect(url_for('home.home'))

@contador_bp.route('/finalizar_pedido', methods=['POST'])
@login_required
def finalizar_pedido():
    if current_user.tipoUsuario != 4:
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('home.home'))

    pedido_id = request.form.get('pedido_id')

    try:
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            flash('Pedido no encontrado', 'error')
            return redirect(url_for('contador.dashboard'))

        if pedido.etapaId != 4:
            flash('Solo se pueden finalizar pedidos en etapa 4', 'error')
            return redirect(url_for('contador.dashboard'))

        pedido.etapaId = 5  # Marcar como entregado
        db.session.commit()
        flash('Pedido marcado como entregado correctamente', 'success')

    except Exception as e:
        flash(f'Error al actualizar pedido: {str(e)}', 'error')

    return redirect(url_for('contador.dashboard'))
