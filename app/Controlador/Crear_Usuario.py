from flask import Blueprint, render_template, request, redirect, url_for, flash
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
        tipo_usuario_id = request.form['tipo_usuario_id']

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            password=password,
            tipoUsuario=tipo_usuario_id
        )

        # Agregar el nuevo usuario a la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Mostrar mensaje de éxito
        flash('Usuario registrado exitosamente.', 'success')

        # Redirigir al formulario de registro nuevamente
        return redirect(url_for('usuario.registrar'))

    # Obtener los tipos de usuario desde la base de datos
    tipos_usuario = TipoUsuario.query.all()
    
    # Renderizar la plantilla de registro
    return render_template('Registro.html', tipos_usuario=tipos_usuario)

# Ruta para registrar un tipo de usuario
@t_usuario_bp.route('/tipo_usuario/registro', methods=['GET', 'POST'])
def registrar_tipo_usuario():
    if request.method == 'POST':
        # Obtener la descripción del tipo de usuario
        descripcion = request.form['descripcion']

        # Crear un nuevo tipo de usuario
        nuevo_tipo_usuario = TipoUsuario(descripcion=descripcion)

        # Agregar el nuevo tipo de usuario a la base de datos
        db.session.add(nuevo_tipo_usuario)
        db.session.commit()

        # Mostrar mensaje de éxito
        flash('Tipo de usuario registrado exitosamente.', 'success')

        # Redirigir al formulario de registro de tipo de usuario
        return redirect(url_for('t_usuario.registrar_tipo_usuario'))

    # Renderizar la plantilla de registro de tipo de usuario
    return render_template('Tipo_Usuario_Registro.html')
