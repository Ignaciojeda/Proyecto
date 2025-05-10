from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.Modelo.Pedido import Pedido
from datetime import datetime, timedelta

contador_bp = Blueprint('contador', __name__)

@contador_bp.route('/contador')
@login_required
def dashboard():
    if current_user.tipoUsuario != 4:  # Asumiendo que 4 es el ID para contadores
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('home'))
    
    hoy = datetime.now()
    inicio_mes = hoy.replace(day=1)
    
    # Estadísticas financieras
    pedidos_mes = Pedido.query.filter(
        Pedido.fechaPedido >= inicio_mes
    ).all()
    
    total_ventas = sum(p.total for p in pedidos_mes)
    num_pedidos = len(pedidos_mes)
    
    # Pedidos pendientes de facturación
    pedidos_pendientes = Pedido.query.filter_by(
        facturado=False
    ).order_by(Pedido.fechaPedido.desc()).limit(10).all()
    
    return render_template('vista_contador.html',
                         total_ventas=total_ventas,
                         num_pedidos=num_pedidos,
                         pedidos_pendientes=pedidos_pendientes)