from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.Modelo.Pedido import Pedido
from app.Modelo.EtapaPedido import EtapaPedido
from app.Modelo.Inventario import Inventario
from app.Modelo.Sucursal import Sucursal
from app.Modelo.DetallePedido import DetallePedido
from app.Modelo.Producto import Producto
from datetime import datetime

bodeguero_bp = Blueprint('bodeguero', __name__)

@bodeguero_bp.route('/bodeguero')
@login_required
def dashboard():
    # Verificar rol de bodeguero
    if current_user.tipoUsuario != 3:
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('home'))

    try:
        # Obtener sucursal asignada al bodeguero
        sucursal = Sucursal.query.filter_by(encargadoId=current_user.idUsuario).first()
        if not sucursal:
            flash('No tienes una sucursal asignada', 'error')
            return redirect(url_for('home'))

        # Obtener pedidos con relaciones cargadas
        pedidos = db.session.query(Pedido)\
            .filter_by(sucursalID=sucursal.sucursalId)\
            .options(
                db.joinedload(Pedido.cliente),
                db.joinedload(Pedido.etapa),
                db.joinedload(Pedido.detalles).joinedload(DetallePedido.producto)
            )\
            .order_by(Pedido.fechaPedido.desc())\
            .all()

        # Obtener inventario
        inventario = db.session.query(Inventario)\
            .filter_by(sucursal_id=sucursal.sucursalId)\
            .join(Producto)\
            .options(db.joinedload(Inventario.producto))\
            .all()

        # Calcular estados de pedidos
        etapas = EtapaPedido.query.all()
        estados = {
            etapa.descripcion: Pedido.query.filter_by(
                sucursalID=sucursal.sucursalId,
                etapaId=etapa.idEtapaPedido
            ).count()
            for etapa in etapas
        }

        return render_template(
            'vista_bodeguero.html',
            sucursal=sucursal,
            pedidos=pedidos,
            inventario=inventario,
            estados=estados,
            current_time=datetime.now()
        )

    except Exception as e:
        flash(f'Error al cargar el panel: {str(e)}', 'error')
        return redirect(url_for('home'))
    
@bodeguero_bp.route('/actualizar_estado', methods=['POST'])
@login_required
def actualizar_estado():
    if current_user.tipoUsuario != 3:
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('bodeguero.dashboard'))
    
    pedido_id = request.form.get('pedido_id')
    nuevo_estado = request.form.get('nuevo_estado')
    
    if not pedido_id or not nuevo_estado:
        flash('Datos incompletos para actualizar el estado', 'error')
        return redirect(url_for('bodeguero.dashboard'))
    
    try:
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            flash('Pedido no encontrado', 'error')
            return redirect(url_for('bodeguero.dashboard'))
        
        # Verificar que el pedido pertenece a la sucursal del bodeguero
        sucursal_bodeguero = Sucursal.query.filter_by(encargadoId=current_user.idUsuario).first()
        if pedido.sucursalID != sucursal_bodeguero.sucursalId:
            flash('No tienes permisos para modificar este pedido', 'error')
            return redirect(url_for('bodeguero.dashboard'))
        
        # Actualizar estado
        pedido.etapaId = nuevo_estado
        db.session.commit()
        
        flash('Estado del pedido actualizado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar el estado: {str(e)}', 'error')
    
    return redirect(url_for('bodeguero.dashboard'))

@bodeguero_bp.route('/actualizar_inventario', methods=['POST'])
@login_required
def actualizar_inventario():
    if current_user.tipoUsuario != 3:
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('bodeguero.dashboard'))
    
    producto_id = request.form.get('producto_id')
    cantidad = request.form.get('cantidad', type=int)
    
    if not producto_id or cantidad is None or cantidad < 0:
        flash('Datos de inventario inválidos', 'error')
        return redirect(url_for('bodeguero.dashboard'))
    
    try:
        # Obtener la sucursal del bodeguero
        sucursal = Sucursal.query.filter_by(encargadoId=current_user.idUsuario).first()
        if not sucursal:
            flash('No tienes una sucursal asignada', 'error')
            return redirect(url_for('bodeguero.dashboard'))
        
        # Actualizar inventario
        inventario = Inventario.query.filter_by(
            sucursal_id=sucursal.sucursalId,
            producto_id=producto_id
        ).first()
        
        if inventario:
            inventario.stock = cantidad
        else:
            inventario = Inventario(
                sucursal_id=sucursal.sucursalId,
                producto_id=producto_id,
                stock=cantidad
            )
            db.session.add(inventario)
        
        db.session.commit()
        flash('Inventario actualizado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar el inventario: {str(e)}', 'error')
    
    return redirect(url_for('bodeguero.dashboard', tab='inventario'))