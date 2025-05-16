from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app import db
from datetime import datetime
from app.Modelo.Pedido import Pedido
from app.Modelo.DetallePedido import DetallePedido
from app.Modelo.EtapaPedido import EtapaPedido

pedidos_bp = Blueprint('pedidos', __name__, template_folder='templates')

@pedidos_bp.route('/')
@login_required
def ver_pedidos():
    # Obtener los pedidos del usuario actual con sus relaciones
    pedidos = db.session.query(Pedido)\
        .filter_by(clienteId=current_user.idUsuario)\
        .join(EtapaPedido)\
        .options(
            db.joinedload(Pedido.detalles).joinedload(DetallePedido.producto),
            db.joinedload(Pedido.sucursal)
        )\
        .order_by(Pedido.fechaPedido.desc())\
        .all()
    
    return render_template('pedidos.html', pedidos=pedidos)

@pedidos_bp.route('/pedidos/<int:pedido_id>')
@login_required
def detalle_pedido(pedido_id):
    # Obtener el pedido con todas las relaciones necesarias
    pedido = db.session.query(Pedido)\
        .filter_by(idPedido=pedido_id)\
        .join(EtapaPedido)\
        .options(
            db.joinedload(Pedido.detalles).joinedload(DetallePedido.producto),
            db.joinedload(Pedido.sucursal)
        )\
        .first_or_404()
    
    # Verificar que el pedido pertenece al usuario actual
    if pedido.clienteId != current_user.idUsuario:
        abort(403)
    
    # Formatear la fecha
    fecha_formateada = pedido.fechaPedido.strftime('%d/%m/%Y a las %H:%M')
    
    return render_template('detalle_pedido.html', 
                         pedido=pedido,
                         fecha_formateada=fecha_formateada)