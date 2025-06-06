from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.Modelo.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Ya estás autenticado como {current_user.email}. Redirigiendo...', 'info')
        if current_user.tipo:
            if current_user.tipo.descripcion == 'Admin':
                return redirect(url_for('admin.dashboard'))  
            elif current_user.tipo.descripcion == 'Cliente':
                return redirect(url_for('home.home'))
            elif current_user.tipo.descripcion == 'Contador':
                return redirect(url_for('contador.dashboard'))
            elif current_user.tipo.descripcion == 'Bodeguero':
                return redirect(url_for('bodeguero.dashboard'))
        else:
            flash('No se pudo determinar el tipo de usuario.', 'danger')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        flash(f'Intentando iniciar sesión con el correo: {email}', 'info')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            flash(f'Usuario encontrado: {usuario.email}', 'info')
            if usuario.check_password(password):
                flash('Contraseña correcta.', 'success')
                login_user(usuario, remember=True)
                if usuario.tipo:
                    if usuario.tipo.descripcion == 'Admin':
                        flash('Redirigiendo al panel de administrador...', 'info')
                        return redirect(url_for('admin.dashboard'))  
                    elif usuario.tipo.descripcion == 'Cliente':
                        flash('Redirigiendo al panel de cliente...', 'info')
                        return redirect(url_for('home.home'))
                    elif usuario.tipo.descripcion == 'Bodeguero':
                        flash('Redirigiendo al panel de bodeguero...', 'info')
                        return redirect(url_for('bodeguero.dashboard'))
                    elif usuario.tipo.descripcion == 'Contador':
                        flash('Redirigiendo al panel de contador...', 'info')
                        return redirect(url_for('contador.dashboard'))
                    elif usuario.tipo.descripcion == 'Vendedor':
                        flash('Redirigiendo al panel de cliente...', 'info')
                        return redirect(url_for('auth.home_vendedor'))                   
                    else:
                        flash('Tipo de usuario no válido.', 'danger')
                        return redirect(url_for('auth.login'))
                else:
                    flash('No se pudo determinar el tipo de usuario.', 'danger')
            else:
                flash('Contraseña incorrecta.', 'danger')

                print("Password ingresada:", password)
                print("Password guardada:", usuario.password)
                print("Resultado check:", check_password_hash(usuario.password, password))
        else:
            flash('Usuario no encontrado.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/vendedor')
@login_required
def home_vendedor():
    return render_template('Vista_Vendedor.html')

API_KEY = "AIzaSyBQ0DDplgatpypYLs0He7N81bLnrOxuBOQ" 

@auth_bp.route("/ingreso_direccion")
def ingreso_direccion():
    return render_template("Ingreso_Direccion.html", api_key=API_KEY)

@auth_bp.route("/get_api_key")
def get_api_key():
    return jsonify({"api_key": API_KEY})

