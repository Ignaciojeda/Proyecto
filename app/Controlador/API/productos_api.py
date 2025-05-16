from flask import Blueprint, jsonify
from app import db
from app.Modelo.Producto import Producto
from app.Modelo.Marca import Marca
from app.Modelo.PrecioProducto import PrecioProducto
from flask_cors import CORS

api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp)  # Habilita CORS para consumo externo

# GET /api/productos
@api_bp.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    resultado = []

    for p in productos:
        precios = PrecioProducto.query.filter_by(productoId=p.idProducto).all()
        precios_formateados = [
            {
                "Fecha": precio.fecha.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                "Valor": float(precio.valor)
            } for precio in precios
        ]

        resultado.append({
            "Código del producto": p.codigoInterno,
            "Marca": p.marca.nombre,
            "Código": p.codigoFabricante,
            "Nombre": p.nombre,
            "Stock": p.stock,
            "Precio": precios_formateados
        })

    return jsonify(resultado)

# GET /api/productos/<codigo>
@api_bp.route('/productos/<string:codigo>', methods=['GET'])
def obtener_producto_por_codigo(codigo):
    producto = Producto.query.filter_by(codigoInterno=codigo).first_or_404()
    precios = PrecioProducto.query.filter_by(productoId=producto.idProducto).all()
    precios_formateados = [
        {
            "Fecha": precio.fecha.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "Valor": float(precio.valor)
        } for precio in precios
    ]

    resultado = {
        "Código del producto": producto.codigoInterno,
        "Marca": producto.marca.nombre,
        "Código": producto.codigoFabricante,
        "Nombre": producto.nombre,
        "Stock": producto.stock,
        "Precio": precios_formateados
    }

    return jsonify(resultado)
