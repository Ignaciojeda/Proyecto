from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/', methods=['GET', 'POST'])
@login_required
def mostrar_perfil():
    if request.method == 'POST':
        try:
            # Actualizar datos del usuario
            current_user.nombre = request.form.get('nombre')
            current_user.apellido = request.form.get('apellido')
            current_user.telefono = request.form.get('telefono')
            
            db.session.commit()
            flash('Tus datos se han actualizado correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar los datos: {str(e)}', 'error')
        
        return redirect(url_for('perfil.mostrar_perfil'))
    
    return render_template('perfil.html')