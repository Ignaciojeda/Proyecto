from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.Modelo.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])  
def login():
    if request.method == 'POST':
        correo_usuario = request.form['correo']
        contraseña = request.form['contraseña']

        
        usuario = Usuario.query.filter_by(correo_usuario=correo_usuario).first()

        
        if usuario and usuario.check_password(contraseña): 
            login_user(usuario)
            return redirect(url_for('listar.lista_objetos'))  
        else:
            flash('Credenciales incorrectas', 'danger') 

    return render_template('login.html')  

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
