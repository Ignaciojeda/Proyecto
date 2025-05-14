from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.Modelo.Producto import Producto
from app.Modelo.Pedido import Pedido
from app import db

vendedor_bp = Blueprint('vendedor', __name__, url_prefix='/vendedor')

@vendedor_bp.route('/')
@login_required
def dashboard():
    # Verificar rol de usuario
    if current_user.tipoUsuario != 3:  # 3 = Vendedor
        flash('No tienes permisos para acceder a esta sección', 'error')
        return redirect(url_for('home.home'))
    
    # Obtener productos disponibles
    productos = Producto.query.filter(Producto.stock > 0).all()
    
    # Obtener pedidos pendientes
    pedidos = Pedido.query.filter_by(estado='pendiente').order_by(Pedido.fecha_creacion.desc()).all()
    
    return render_template('Vista_Vendedor.html', 
                         productos=productos, 
                         pedidos=pedidos)

@vendedor_bp.route('/aprobar_pedido/<int:pedido_id>')
@login_required
def aprobar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'aprobado'
    db.session.commit()
    flash('Pedido aprobado correctamente', 'success')
    return redirect(url_for('vendedor.dashboard'))

@vendedor_bp.route('/rechazar_pedido/<int:pedido_id>')
@login_required
def rechazar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'rechazado'
    db.session.commit()
    flash('Pedido rechazado correctamente', 'warning')
    return redirect(url_for('vendedor.dashboard'))

@vendedor_bp.route('/enviar_bodega/<int:pedido_id>')
@login_required
def enviar_bodega(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'en_bodega'
    db.session.commit()
    flash('Pedido enviado a bodega para preparación', 'info')
    return redirect(url_for('vendedor.dashboard'))