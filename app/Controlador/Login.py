from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.Modelo.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])  # Esta es la ruta principal que usas para el login
def login():
    if request.method == 'POST':
        correo_usuario = request.form['correo']
        contraseña = request.form['contraseña']

        # Buscar usuario en la base de datos
        usuario = Usuario.query.filter_by(correo_usuario=correo_usuario).first()

        # Verificar contraseña
        if usuario and usuario.contraseña == contraseña:  # Cambiado para comparar directamente
            login_user(usuario)
            return redirect(url_for('listar.lista_objetos'))  # Redirigir a listar_objetos
        else:
            flash('Credenciales incorrectas', 'danger')  # Mensaje de error

    return render_template('home.html')  # Regresar a la misma página en caso de error

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
