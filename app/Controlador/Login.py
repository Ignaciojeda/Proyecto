from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.Modelo.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Ya estás autenticado como {current_user.email}. Redirigiendo...', 'info')
        if current_user.tipo:
            if current_user.tipo.descripcion == 'Admin':
                return redirect(url_for('auth.home_admin'))
            elif current_user.tipo.descripcion == 'Cliente':
                return redirect(url_for('auth.home_usuario'))
        else:
            flash('No se pudo determinar el tipo de usuario.', 'danger')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        flash(f'Intentando iniciar sesión con el correo: {email}', 'info')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            flash(f'Usuario encontrado: {usuario.email}', 'info')
            if usuario.check_password(password):
                flash('Contraseña correcta.', 'success')
                login_user(usuario)
                if usuario.tipo:
                    if usuario.tipo.descripcion == 'Admin':
                        flash('Redirigiendo al panel de administrador...', 'info')
                        return redirect(url_for('auth.home_admin'))
                    elif usuario.tipo.descripcion == 'Cliente':
                        flash('Redirigiendo al panel de cliente...', 'info')
                        return redirect(url_for('auth.home_usuario'))
                    else:
                        flash('Tipo de usuario no válido.', 'danger')
                        return redirect(url_for('auth.login'))
                else:
                    flash('No se pudo determinar el tipo de usuario.', 'danger')
            else:
                flash('Contraseña incorrecta.', 'danger')

                print("Password ingresada:", password)
                print("Password guardada:", usuario.password)
                print("Resultado check:", check_password_hash(usuario.password, password))
        else:
            flash('Usuario no encontrado.', 'danger')

    return render_template('login.html')

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
