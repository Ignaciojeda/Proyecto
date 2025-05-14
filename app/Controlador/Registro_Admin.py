from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.Modelo.Usuario import Usuario
from app.Modelo.TipoUsuario import TipoUsuario
from app import db
from werkzeug.security import generate_password_hash

admin_registro_bp = Blueprint('admin_registro', __name__)

@admin_registro_bp.route('/admin/registro', methods=['GET', 'POST'])
@login_required
def registrar_admin():
    # Verificar que el usuario actual es administrador
    if current_user.tipoUsuario != 2:  # Asumiendo que 1 es el ID para administradores
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('home'))
    
    tipos_usuario = TipoUsuario.query.all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        password = request.form.get('password')
        tipo_usuario = request.form.get('tipo_usuario')
        
        if Usuario.query.filter_by(email=email).first():
            flash('Este correo ya está registrado', 'error')
            return redirect(url_for('admin_registro.registrar_admin'))
        
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            password=generate_password_hash(password),
            tipoUsuario=tipo_usuario
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('registro_admin.html', tipos_usuario=tipos_usuario)