from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.Modelo.Pedido import Pedido
from app.Modelo.Usuario import Usuario
from app.Modelo.EtapaPedido import EtapaPedido
from app.Modelo.DetallePedido import DetallePedido
from app.Modelo.Producto import Producto
from sqlalchemy import func
from datetime import date, datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def dashboard():
    # Verificación de admin
    if not current_user.tipo or current_user.tipo.descripcion != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('auth.login'))

    try:
        # Estadísticas principales (totales)
        ventas_totales = db.session.query(func.coalesce(func.sum(Pedido.total), 0)).scalar()
        pedidos_totales = Pedido.query.count()
        usuarios_registrados = Usuario.query.count()

        # Estadísticas detalladas de pedidos por etapa
        etapas = EtapaPedido.query.all()
        estados_pedidos = {
            etapa.descripcion: Pedido.query.filter_by(etapaId=etapa.idEtapaPedido).count()
            for etapa in etapas
        }

        # Pedidos recientes con relaciones cargadas
        pedidos_recientes = db.session.query(Pedido)\
            .options(
                db.joinedload(Pedido.cliente),
                db.joinedload(Pedido.etapa),
                db.joinedload(Pedido.detalles).joinedload(DetallePedido.producto)
            )\
            .order_by(Pedido.fechaPedido.desc())\
            .limit(10)\
            .all()

        return render_template('Home_Admin.html',
            ventas_hoy=ventas_totales,          # Nota: puedes renombrar también en el template para claridad
            pedidos_hoy=pedidos_totales,
            total_usuarios=usuarios_registrados,
            pedidos_recientes=pedidos_recientes,
            estados=estados_pedidos,
            hoy=date.today().strftime('%d/%m/%Y'),
            current_time=datetime.now()
        )

    except Exception as e:
        flash(f'Error al cargar datos: {str(e)}', 'error')
        # Versión de respaldo con valores por defecto
        return render_template('Home_Admin.html',
            ventas_hoy=0,
            pedidos_hoy=0,
            total_usuarios=0,
            pedidos_recientes=[],
            estados={},
            hoy=date.today().strftime('%d/%m/%Y'),
            current_time=datetime.now()
        )
