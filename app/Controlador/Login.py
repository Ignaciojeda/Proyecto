from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.Modelo.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Verificamos el tipo de usuario directamente
        if current_user.tipo_usuario == 1:  # 1 corresponde a Admin
            return redirect(url_for('auth.home_admin'))
        elif current_user.tipo_usuario == 2:  # 2 corresponde a Usuario
            return redirect(url_for('auth.home_usuario'))
    
    if request.method == 'POST':
        correo_usuario = request.form['correo']
        contraseña = request.form['contraseña']

        # Usamos 'correo' para la búsqueda
        usuario = Usuario.query.filter_by(correo=correo_usuario).first()

        if usuario and usuario.check_password(contraseña):  # Asumimos que check_password está correcto
            login_user(usuario)
            # Verificamos el tipo de usuario para redirigir
            if usuario.tipo_usuario == 1:  # 1 corresponde a Admin
                return redirect(url_for('auth.home_admin'))
            elif usuario.tipo_usuario == 2:  # 2 corresponde a Usuario
                return redirect(url_for('auth.home_usuario'))
            else:
                flash('No se ha definido un tipo de usuario válido.', 'danger')
                return redirect(url_for('auth.login'))

        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template('home.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/home_admin')
@login_required
def home_admin():
    return render_template('Home_Admin.html')

@auth_bp.route('/home_usuario')
@login_required
def home_usuario():
    return render_template('Home.html')
