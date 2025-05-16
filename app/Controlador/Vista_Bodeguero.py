from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.Modelo.Pedido import Pedido
from app.Modelo.EtapaPedido import EtapaPedido
from app.Modelo.Inventario import Inventario
from app.Modelo.DetallePedido import DetallePedido
from app.Modelo.Producto import Producto
from datetime import datetime

bodeguero_bp = Blueprint('bodeguero', __name__)

@bodeguero_bp.route('/')
@login_required
def dashboard():
    print("Entrando a la vista del bodeguero")

    if current_user.tipoUsuario != 3:
        print("Usuario no autorizado:", current_user.tipoUsuario)
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('home.home'))

    try:
        print("Usuario autorizado:", current_user.nombre)

        pedidos = db.session.query(Pedido)\
            .options(
                db.joinedload(Pedido.cliente),
                db.joinedload(Pedido.etapa),
                db.joinedload(Pedido.detalles).joinedload(DetallePedido.producto)
            )\
            .order_by(Pedido.fechaPedido.desc())\
            .all()

        print(f"{len(pedidos)} pedidos encontrados.")
        for p in pedidos:
            print(f"Pedido {p.idPedido} - Estado: {p.etapa.descripcion if p.etapa else 'Sin etapa'}")

        # Obtener todo el inventario
        inventario = db.session.query(Inventario)\
            .join(Producto)\
            .options(db.joinedload(Inventario.producto))\
            .all()
        print(f"{len(inventario)} productos en inventario total.")

        # Calcular estados resumidos según etapaId
        pendientes = Pedido.query.filter_by(etapaId=1).count()
        preparacion = Pedido.query.filter(Pedido.etapaId.in_([2, 3])).count()
        listos = Pedido.query.filter_by(etapaId=4).count()

        estados = {
            'Pendientes': pendientes,
            'Preparacion': preparacion,
            'Listos': listos
        }

        print(f"Pedidos Pendientes: {pendientes}")
        print(f"En Preparación: {preparacion}")
        print(f"Listos para despacho: {listos}")

        return render_template(
            'vista_bodeguero.html',
            pedidos=pedidos,
            inventario=inventario,
            estados=estados,
            current_time=datetime.now()
        )

    except Exception as e:
        print("Error en dashboard:", str(e))
        flash(f'Error al cargar el panel: {str(e)}', 'error')
        return redirect(url_for('bodeguero.dashboard'))


@bodeguero_bp.route('/actualizar_estado', methods=['POST'])
@login_required
def actualizar_estado():
    if current_user.tipoUsuario != 3:
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('home.home'))

    pedido_id = request.form.get('pedido_id')
    nuevo_estado = int(request.form.get('nuevo_estado'))

    try:
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            flash('Pedido no encontrado', 'error')
            return redirect(url_for('bodeguero.dashboard'))

        estado_actual = pedido.etapaId
        print(f"Pedido {pedido.idPedido} - Estado actual: {estado_actual}, nuevo estado solicitado: {nuevo_estado}")

        # Solo permitir cambio secuencial y nunca al estado 5
        if nuevo_estado == 5:
            flash('El bodeguero no puede marcar como entregado', 'error')
        elif nuevo_estado == estado_actual + 1 and nuevo_estado <= 4:
            pedido.etapaId = nuevo_estado
            db.session.commit()
            flash('Estado del pedido actualizado correctamente', 'success')
        else:
            flash('No se permite esta transición de estado', 'error')

    except Exception as e:
        print("Error al actualizar estado:", str(e))
        flash('Error al actualizar el estado del pedido', 'error')

    return redirect(url_for('bodeguero.dashboard'))