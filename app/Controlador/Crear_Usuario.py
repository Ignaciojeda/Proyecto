from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import db
from app.Modelo.Usuario import Usuario
from app.Modelo.TipoUsuario import TipoUsuario

# Definir los blueprints
usuario_bp = Blueprint('usuario', __name__)
t_usuario_bp = Blueprint('t_usuario', __name__)

# Ruta para registrar un usuario
@usuario_bp.route('/registro', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        password = request.form['password']
        tipoUsuario_str = request.form['tipoUsuario']

        # Validar que todos los campos obligatorios estén completos
        if not nombre or not email or not password or not tipoUsuario_str:
            flash('Por favor completa todos los campos obligatorios.', 'error')
            return redirect(url_for('usuario.registrar'))

        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('Ya existe un usuario con ese correo.', 'error')
            return redirect(url_for('usuario.registrar'))

     

        # Convertir tipoUsuario a entero
        try:
            tipoUsuario = int(tipoUsuario_str)  # Asegúrate de que tipoUsuario es un número entero
        except ValueError:
            flash('Tipo de usuario inválido.', 'error')
            return redirect(url_for('usuario.registrar'))

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            password=password,
            tipoUsuario=tipoUsuario   
        ) 

        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'error')

        return redirect(url_for('usuario.registrar'))

    
    tipos_usuario = TipoUsuario.query.all()
    return render_template('Registro.html', tipos_usuario=tipos_usuario)



