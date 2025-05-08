from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.Modelo.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.tipo.descripcion == 'Admin':
            return redirect(url_for('auth.home_admin'))
        elif current_user.tipo.descripcion == 'Cliente':
            return redirect(url_for('auth.home_usuario'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash('Inicio de sesión exitoso.', 'success')
            if usuario.tipo.descripcion == 'Admin':
                return redirect(url_for('auth.home_admin'))
            elif usuario.tipo.descripcion == 'Cliente':
                return redirect(url_for('auth.home_usuario'))
            else:
                flash('Tipo de usuario no válido.', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Credenciales incorrectas.', 'danger')

    return render_template('home.html')

@auth_bp.route('/logout')
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
