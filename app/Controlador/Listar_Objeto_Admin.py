from flask import Blueprint, render_template, abort, request, url_for, flash, redirect
from flask_login import login_required, current_user
from app.Modelo.Objeto_Perdido import ObjetoPerdido
from app.Modelo.Historial import Historial
from app import db

# Crear el Blueprint
listara_bp = Blueprint('listara', __name__)

# Ruta para listar objetos (solo admins)
@listara_bp.route('/listar_objeto_admin')
@login_required
def lista_objetos_admin():
    if current_user.tipo_usuario != 1: 
        flash('No tienes permisos para acceder a esta página.', 'error')
        return redirect(url_for('home')) 

    try:
        objetos = ObjetoPerdido.query.filter_by(activo=True).all()
        print(objetos)  # Verifica qué datos se obtienen
        return render_template('Listar_Objeto_Admin.html', objetos=objetos)
    except Exception as e:
        print(f"Error al cargar los datos: {e}")  # Mostrar el error en la consola
        flash('Ocurrió un error al cargar los datos.', 'error')
        return redirect(url_for('auth.home_admin'))



