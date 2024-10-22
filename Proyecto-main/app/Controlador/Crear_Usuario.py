from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.Modelo.Usuario import Usuario
from app.Modelo.Tipo_Usuario import TipoUsuario
from flask_login import login_required

usuario_bp = Blueprint('usuario', __name__)
t_usuario_bp = Blueprint('t_usuario', __name__)

@usuario_bp.route('/registro', methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        id_tipo_usuario = request.form['id_tipo_usuario']
        correo_usuario = request.form['correo_usuario']
        contraseña = request.form['contraseña']

        
        nuevo_usuario = Usuario(
            id_tipo_usuario=id_tipo_usuario,
            correo_usuario=correo_usuario,
            contraseña=contraseña  
        )

        
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('usuario.registrar')) 
    
    return render_template('Registro.html')

@t_usuario_bp.route('/registro', methods=['GET', 'POST'])
def t_usuario():
    if request.method == 'POST':
        id_tipo_usuario = request.form['id_usuario']
        descripcion = request.form['descripcion']

        
        nuevo_t_usuario = TipoUsuario(
            id_tipo_usuario=id_tipo_usuario,
            descripcion=descripcion,
        )
        db.session.add(nuevo_t_usuario)
        db.session.commit()

        return redirect(url_for('t_usuario.registrar'))  
    
    return render_template('Tipo_Usuario_Registro.html')
