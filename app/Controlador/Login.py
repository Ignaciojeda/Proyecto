from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.Modelo.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        e
        if current_user.tipo_usuario == 1: 
            return redirect(url_for('auth.home_admin'))
        elif current_user.tipo_usuario == 2:  
            return redirect(url_for('auth.home_usuario'))

    if request.method == 'POST':
        
        correo_usuario = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        
        usuario = Usuario.query.filter_by(correo=correo_usuario).first()

        
        if usuario:
            if usuario.check_password(contraseña):  
                login_user(usuario)
                
                if usuario.tipo_usuario == 1: 
                    return redirect(url_for('auth.home_admin'))
                elif usuario.tipo_usuario == 2:  
                    return redirect(url_for('auth.home_usuario'))
                else:
                    flash('Tipo de usuario no reconocido.', 'danger')
            else:
                flash('Contraseña incorrecta.', 'danger')
        else:
            flash('Usuario no encontrado.', 'danger')

    return render_template('login.html')  

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/home_admin')
@login_required
def home_admin():
    if current_user.tipo_usuario != 1:
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('Home_Admin.html')

@auth_bp.route('/home_usuario')
@login_required
def home_usuario():
    if current_user.tipo_usuario != 2:
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('Home.html')
