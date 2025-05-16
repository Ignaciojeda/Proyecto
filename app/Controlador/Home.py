from flask import Blueprint, render_template
from flask_login import login_required
from app.Modelo.Producto import Producto
from app import db

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home():
    try:
        # Cargar los primeros 6 productos (puedes ajustar el límite)
        productos = Producto.query.limit(6).all()

        return render_template('home.html', productos=productos)

    except Exception as e:
        print(f"[ERROR en home] {str(e)}")
        return render_template('home.html', productos=[])
