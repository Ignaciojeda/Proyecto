from flask import Blueprint, render_template, request, abort, jsonify, current_app
from app.Modelo.Producto import Producto
from app.Modelo.Categoria import Categoria
from app.Modelo.Marca import Marca
from app import db
from datetime import datetime

catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/', methods=['GET'])
def catalogo():
    # Obtener parámetros de filtrado
    categoria = request.args.get('categoria')
    marca = request.args.get('marca')
    precio = request.args.get('precio')
    busqueda = request.args.get('busqueda')
    moneda = request.args.get('moneda', 'CLP')  # Nueva: parámetro de moneda

    # Consulta base
    productos = Producto.query

    # Aplicar filtros
    if categoria and categoria != "Todas":
        productos = productos.join(Producto.categoria).filter(Categoria.nombreCategoria == categoria)

    if marca and marca != "Todas":
        productos = productos.join(Producto.marca).filter(Marca.nombreMarca == marca)

    if busqueda:
        productos = productos.filter(Producto.nombreProducto.ilike(f"%{busqueda}%"))

    if precio and precio != "Todos":
        if precio == "Menos de $10.000":
            productos = productos.filter(Producto.precio < 10000)
        elif precio == "$10.000 - $50.000":
            productos = productos.filter(Producto.precio.between(10000, 50000))
        elif precio == "Más de $50.000":
            productos = productos.filter(Producto.precio > 50000)

    productos = productos.all()

    # Obtener categorías y marcas para los filtros
    categorias = Categoria.query.all()
    marcas = Marca.query.all()

    # Obtener tasas de cambio si no es CLP
    tasas = {}
    if moneda != 'CLP':
        try:
            response = current_app.test_client().get('/api/v1/divisas/tasas')
            if response.status_code == 200:
                tasas = response.json
        except Exception as e:
            current_app.logger.error(f"Error obteniendo tasas: {str(e)}")

    return render_template(
        "catalogo.html",
        productos=productos,
        categorias=categorias,
        marcas=marcas,
        moneda_seleccionada=moneda,
        tasas_cambio=tasas,
        fecha_actualizacion=datetime.now().isoformat()
    )

@catalogo_bp.route('/producto/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    moneda = request.args.get('moneda', 'CLP')
    
    # Obtener tasa de cambio si es necesario
    tasa = None
    if moneda != 'CLP':
        try:
            response = current_app.test_client().get(f'/api/v1/divisas/convertir?monto=1&origen=CLP&destino={moneda}')
            if response.status_code == 200:
                tasa = response.json.get('tasa_cambio')
        except Exception as e:
            current_app.logger.error(f"Error obteniendo tasa: {str(e)}")
    
    return render_template(
        "producto_detalle.html",
        producto=producto,
        moneda_seleccionada=moneda,
        tasa_cambio=tasa
    )