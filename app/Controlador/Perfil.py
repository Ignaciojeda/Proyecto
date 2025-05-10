from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.Modelo.Usuario import Usuario
from app import db

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def mostrar_perfil():
    if request.method == 'POST':
        # Actualizar datos del usuario
        current_user.nombre = request.form.get('nombre')
        current_user.telefono = request.form.get('telefono')
        db.session.commit()
        flash('Tus datos se han actualizado correctamente', 'success')
        return redirect(url_for('perfil.mostrar_perfil'))
    
    return render_template('perfil.html', usuario=current_user)