from flask import Blueprint, render_template, request, redirect, url_for
from app.Modelo.Producto import Producto

catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/catalogo')
def mostrar_catalogo():
    productos = Producto.query.all()
    return render_template('catalogo.html', productos=productos)