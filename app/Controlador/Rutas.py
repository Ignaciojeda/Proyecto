from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

login_bp = Blueprint('login', __name__)  

@login_bp.route('/')
def home():
    # Redirigir a la página correspondiente si el usuario ya está autenticado
    if current_user.is_authenticated:
        if current_user.tipo_usuario.descripcion == 'Admin':
            return redirect(url_for('auth.home_admin'))
        else:
            return redirect(url_for('auth.home'))
    # Si no está autenticado, mostrar la página de login
    return render_template('login.html')
    
