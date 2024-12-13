from flask import Blueprint,render_template, redirect, url_for
from flask_login import login_required
from app import db
from app.Modelo.Historial import Historial
from app.Modelo.Usuario import Usuario
from app.Modelo.Carrera import Carrera

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial', methods=['GET'])
@login_required
def historial():
    # Consulta para obtener el historial con datos del usuario y carrera
    historial_objetos = db.session.query(
        Historial,
        Usuario.nombre_completo,
        Carrera.descripcion
    ) \
    .join(Usuario, Historial.rut_usuario == Usuario.rut) \
    .join(Carrera, Usuario.carrera == Carrera.id_carrera) \
    .filter(Historial.activo == True).all()
    
    # Renderiza la plantilla y pasa los datos del historial
    return render_template('historial.html', historial=historial_objetos)


