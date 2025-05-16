from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app import db
from app.Modelo.Producto import Producto
from app.Modelo.Carrito import Carrito
from datetime import datetime  # 👈 Importamos datetime

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/carrito')
@login_required
def ver_carrito():
    items = Carrito.query.filter_by(usuarioId=current_user.idUsuario).all()
    productos = []
    total = 0

    for item in items:
        producto = Producto.query.get(item.productoId)
        if producto:
            subtotal = item.cantidad * item.precio
            productos.append({
                'producto': producto,
                'cantidad': item.cantidad,
                'precio': item.precio,
                'subtotal': subtotal
            })
            total += subtotal

    # 👇 Creamos el buy_order único con timestamp
    now_str = datetime.now().strftime('%Y%m%d%H%M%S')
    buy_order = f"orden_{current_user.idUsuario}_{now_str}"

    return render_template('Carrito.html', productos=productos, total=total, buy_order=buy_order)

@carrito_bp.route('/agregar/<int:producto_id>', methods=['POST'])
@login_required
def agregar_al_carrito(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    precio = int(request.form.get('precio'))

    carrito_existente = Carrito.query.filter_by(usuarioId=current_user.idUsuario, productoId=producto_id).first()

    if carrito_existente:
        carrito_existente.cantidad += cantidad
        carrito_existente.precio = precio
    else:
        nuevo_carrito = Carrito(
            usuarioId=current_user.idUsuario,
            productoId=producto_id,
            cantidad=cantidad,
            precio=precio
        )
        db.session.add(nuevo_carrito)

    db.session.commit()
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('catalogo.catalogo'))

@carrito_bp.route('/eliminar/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(producto_id):
    cantidad_a_eliminar = int(request.form.get('cantidad', 1))
    
    item = Carrito.query.filter_by(usuarioId=current_user.idUsuario, productoId=producto_id).first()

    if item:
        if cantidad_a_eliminar >= item.cantidad:
            db.session.delete(item)
            flash('Producto eliminado completamente del carrito', 'info')
        else:
            item.cantidad -= cantidad_a_eliminar
            flash(f'Se eliminaron {cantidad_a_eliminar} unidades del producto', 'info')
        db.session.commit()
    else:
        flash('Producto no encontrado en el carrito', 'warning')

    return redirect(url_for('carrito.ver_carrito'))
