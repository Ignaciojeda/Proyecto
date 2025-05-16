from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.Modelo.Usuario import Usuario
from app.Modelo.TipoUsuario import TipoUsuario
from app import db
from werkzeug.security import generate_password_hash

registra_bp = Blueprint('registra', __name__)

@registra_bp.route('/', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        password = request.form.get('password')
        
        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('Este correo ya está registrado', 'error')
            return redirect(url_for('registro.registrar'))
        
        # Crear nuevo usuario (cliente por defecto)
        tipo_cliente = TipoUsuario.query.filter_by(descripcion='Cliente').first()
        
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            password=generate_password_hash(password),
            tipoUsuario=tipo_cliente.idTipoUsuario
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro_admin.html')