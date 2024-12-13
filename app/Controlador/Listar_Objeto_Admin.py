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
        # Obtener todos los objetos perdidos
        objetos = ObjetoPerdido.query.all()
        return render_template('Listar_Objeto_Admin.html', objetos=objetos)
    except Exception as e:
        flash('Ocurrió un error al cargar los datos.', 'error')
        return redirect(url_for('home_admin'))  # Redirige a la página principal de admin

# Ruta para mostrar el formulario de entrega de un objeto
@listara_bp.route('/entregar_objeto/<int:id>', methods=['GET'])
@login_required
def entregar_objeto(id):
    try:
        objeto = ObjetoPerdido.query.get_or_404(id)  # Buscar objeto por ID
        return render_template('entregar_objeto.html', objeto=objeto)
    except Exception as e:
        flash('Ocurrió un error al cargar el objeto.', 'error')
        return redirect(url_for('listara.lista_objetos_admin'))  # Redirige a la lista de objetos


