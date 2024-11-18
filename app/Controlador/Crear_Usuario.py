from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.Modelo.Usuario import Usuario
from app.Modelo.Tipo_Usuario import TipoUsuario
from app.Modelo.Carrera import Carrera

usuario_bp = Blueprint('usuario', __name__)
t_usuario_bp = Blueprint('t_usuario', __name__)

@usuario_bp.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        try:
            rut = request.form['rut']
            nombre_completo = request.form['nombre_completo']
            carrera_id = request.form.get('Carrera')  # Se selecciona la carrera
            correo = request.form['correo']
            contraseña = request.form['contraseña']
            tipo_usuario_id = request.form.get('Tipo_usuario')  # Se selecciona el tipo de usuario

            nuevo_usuario = Usuario(
                rut=rut,
                nombre_completo=nombre_completo,
                carrera=carrera_id,
                correo=correo,
                contraseña=contraseña,
                tipo_usuario=tipo_usuario_id
            )

            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('usuario.registrar_usuario'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')

    carreras = Carrera.query.all()
    tipos_usuario = TipoUsuario.query.all()
    return render_template('Registro.html', carreras=carreras, tipos_usuario=tipos_usuario)

@t_usuario_bp.route('/registro', methods=['GET', 'POST'])
def registrar_tipo_usuario():
    if request.method == 'POST':
        try:
            descripcion = request.form['descripcion']

            nuevo_t_usuario = TipoUsuario(descripcion=descripcion)
            db.session.add(nuevo_t_usuario)
            db.session.commit()
            flash('Tipo de usuario registrado exitosamente.', 'success')
            return redirect(url_for('t_usuario.registrar_tipo_usuario'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el tipo de usuario: {str(e)}', 'danger')

    return render_template('Tipo_Usuario_Registro.html')
