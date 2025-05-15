from flask import Blueprint, render_template, request, abort
from app.Modelo.Producto import Producto
from app.Modelo.Categoria import Categoria
from app.Modelo.Marca import Marca
from app import db

catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/', methods=['GET'])
def catalogo():
    categoria = request.args.get('categoria')
    marca = request.args.get('marca')
    precio = request.args.get('precio')
    busqueda = request.args.get('busqueda')

    productos = Producto.query

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

    categorias = Categoria.query.all()
    marcas = Marca.query.all()

    return render_template("catalogo.html", productos=productos, categorias=categorias, marcas=marcas)


@catalogo_bp.route('/producto/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
    # Obtiene el producto por su ID
    producto = Producto.query.get(producto_id)

    if not producto:
        abort(404)  # Si el producto no existe, se envía un error 404

    # Renderiza la plantilla de detalle y le pasa el producto obtenido
    return render_template("producto_detalle.html", producto=producto)