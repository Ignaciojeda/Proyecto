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
        return redirect(url_for('home.home'))  # Ajustado si el endpoint es home.home

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

        # Obtener todo el inventario sin filtrar por sucursal
        inventario = db.session.query(Inventario)\
            .join(Producto)\
            .options(db.joinedload(Inventario.producto))\
            .all()
        print(f"{len(inventario)} productos en inventario total.")

        # Contar cantidad de pedidos por etapa
        etapas = EtapaPedido.query.all()
        estados = {}
        for etapa in etapas:
            cantidad = Pedido.query.filter_by(etapaId=etapa.idEtapaPedido).count()
            estados[etapa.descripcion] = cantidad
            print(f"Estado '{etapa.descripcion}': {cantidad} pedidos")

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
