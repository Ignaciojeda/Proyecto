from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app import db
from app.Modelo.Objeto_Perdido import ObjetoPerdido
from app.Modelo.Objeto_Perdido import Usuario  

objeto_bp = Blueprint('objeto', __name__)
auth_bp = Blueprint('auth', __name__)
home_bp = Blueprint('home', __name__)

@objeto_bp.route('/subir_objeto', methods=['GET', 'POST'])
def subir_objeto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        foto = request.files['foto'].read()  # Lee el archivo como binario
        sala_encontrada = request.form['sala_encontrada']
        hora_encontrada = request.form['hora_encontrada']
        fecha_encontrada = request.form['fecha_encontrada']

        nuevo_objeto = ObjetoPerdido(
            nombre=nombre,
            descripcion=descripcion,
            foto=foto,
            sala_encontrada=sala_encontrada,
            hora_encontrada=hora_encontrada,
            fecha_encontrada=fecha_encontrada
        )

        # Guardar en la base de datos
        db.session.add(nuevo_objeto)
        db.session.commit()
        
        return redirect(url_for('objeto.subir_objeto'))

    return render_template('Subir_Objeto.html')


@objeto_bp.route('/eliminar_objeto/<int:id>', methods=['POST'])
def eliminar_objeto(id):
    # Verifica si el usuario está en la sesión
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])  # Obtener el usuario desde la base de datos usando la sesión
        # Verifica si el usuario es de tipo admin
        if usuario.tipo_usuario.descripcion != 'admin':
            flash('No tienes permiso para eliminar objetos.', 'danger')
            return redirect(url_for('listar.lista_objetos'))

    # Buscar el objeto en la base de datos por su id
    objeto = ObjetoPerdido.query.get_or_404(id)

    try:
        # Eliminar el objeto de la base de datos
        db.session.delete(objeto)
        db.session.commit()
        flash('El objeto ha sido eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el objeto: {str(e)}', 'danger')

    # Redirigir a la lista de objetos después de eliminar
    return redirect(url_for('listar.lista_objetos'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        contraseña = request.form['contraseña']

        # Buscar al usuario en la base de datos
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario is None or not usuario.check_password(contraseña):
            flash('Nombre de usuario o contraseña incorrectos.')
            return redirect(url_for('auth.login'))
        
        # Si el login es exitoso, guardar los datos en la sesión
        session['username'] = usuario.username
        session['role'] = usuario.role  # Guardar el rol del usuario en la sesión

        # Redireccionar al home correspondiente según el rol
        if usuario.role == 'admin':
            return redirect(url_for('home.home_admin'))  # Ruta para admin
        else:
            return redirect(url_for('home.home'))  # Ruta para estudiante

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.')
    return redirect(url_for('auth.login'))

@home_bp.route('/home', methods=['GET'])
def home():
    if 'username' in session and session['role'] == 'estudiante':
        return render_template('home.html')
    else:
        flash('No tienes permisos para acceder a esta página.')
        return redirect(url_for('auth.login'))  # Redirige al login si no es estudiante

# Página para administradores
@home_bp.route('/home_admin', methods=['GET'])
def home_admin():
    if 'username' in session and session['role'] == 'admin':
        return render_template('home_admin.html')
    else:
        flash('No tienes permisos para acceder a esta página.')
        return redirect(url_for('auth.login'))  # Redirige al login si no es admin