from flask import Blueprint, render_template
from app.Modelo.Producto import Producto

catalogo_bp = Blueprint('catalogo', __name__)  # Nombre importante!

@catalogo_bp.route('/')  # Usa solo '/' porque el prefijo ya está en el registro
def mostrar_catalogo():
    productos = Producto.query.all()
    return render_template('catalogo.html', productos=productos)