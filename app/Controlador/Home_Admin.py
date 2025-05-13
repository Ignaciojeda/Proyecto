from flask import Blueprint, render_template
from flask_login import login_required
from app.Modelo.Pedido import Pedido
from app.Modelo.Usuario import Usuario
from app.Modelo.Producto import Producto
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('')
@login_required
def dashboard():
    # Estadísticas para el dashboard
    hoy = datetime.now()
    inicio_mes = hoy.replace(day=1)
    
    total_ventas = Pedido.query.filter(
        Pedido.fechaPedido >= inicio_mes
    ).count()
    
    total_usuarios = Usuario.query.count()
    total_productos = Producto.query.count()
    
    pedidos_recientes = Pedido.query.order_by(
        Pedido.fechaPedido.desc()
    ).limit(5).all()
    
    return render_template('home_admin.html', 
                         total_ventas=total_ventas,
                         total_usuarios=total_usuarios,
                         total_productos=total_productos,
                         pedidos_recientes=pedidos_recientes)