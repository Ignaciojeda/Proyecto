from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from app.Modelo.Producto import Producto
# from app.Modelo.Carrito import Carrito

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/carrito')
@login_required
def ver_carrito():
    if 'carrito' not in session:
        session['carrito'] = {}
    
    # Obtener detalles de productos en el carrito
    productos = []
    total = 0
    for producto_id, cantidad in session['carrito'].items():
        producto = Producto.query.get(producto_id)
        if producto:
            productos.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': producto.precio * cantidad
            })
            total += producto.precio * cantidad
    
    return render_template('carrito.html', productos=productos, total=total)

@carrito_bp.route('/agregar/<int:producto_id>', methods=['POST'])
@login_required
def agregar_al_carrito(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    
    if 'carrito' not in session:
        session['carrito'] = {}
    
    if str(producto_id) in session['carrito']:
        session['carrito'][str(producto_id)] += cantidad
    else:
        session['carrito'][str(producto_id)] = cantidad
    
    session.modified = True
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('catalogo.mostrar_catalogo'))

@carrito_bp.route('/eliminar/<int:producto_id>')
@login_required
def eliminar_del_carrito(producto_id):
    if 'carrito' in session and str(producto_id) in session['carrito']:
        del session['carrito'][str(producto_id)]
        session.modified = True
        flash('Producto eliminado del carrito', 'info')
    
    return redirect(url_for('carrito.ver_carrito'))