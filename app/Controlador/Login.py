from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.Modelo.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])  
def login():
    if request.method == 'POST':
        correo_usuario = request.form['correo']
        contraseña = request.form['contraseña']

        # Buscar usuario en la base de datos
        usuario = Usuario.query.filter_by(correo_usuario=correo_usuario).first()

        # Verificar la contraseña usando check_password
        if usuario and usuario.check_password(contraseña):  
            login_user(usuario)

            # Verificar el tipo de usuario y redirigir según el tipo
            if usuario.tipo_usuario.nombre == 'Admin':  
                return render_template('admin.html')  
            elif usuario.tipo_usuario.nombre == 'Usuario':  
                return render_template('hub.html')  
            else:
                flash('No se ha definido un tipo de usuario válido.', 'danger')
                return redirect(url_for('auth.login'))

        else:
            flash('Credenciales incorrectas', 'danger')  # Mensaje de error si las credenciales fallan

    return render_template('home.html')  # Página de inicio de sesión

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
