from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.Modelo.Pedido import Pedido

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos')
@login_required
def ver_pedidos():
    pedidos = Pedido.query.filter_by(clienteId=current_user.idUsuario).order_by(
        Pedido.fechaPedido.desc()
    ).all()
    
    return render_template('pedidos.html', pedidos=pedidos)

@pedidos_bp.route('/pedidos/<int:pedido_id>')
@login_required
def detalle_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    
    # Verificar que el pedido pertenece al usuario actual
    if pedido.clienteId != current_user.idUsuario:
        abort(403)
    
    return render_template('detalle_pedido.html', pedido=pedido)