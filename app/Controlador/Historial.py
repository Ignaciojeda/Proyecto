from flask import Blueprint,render_template, redirect, url_for
from flask_login import login_required
from app import db
from app.Modelo.Historial import Historial
from app.Modelo.Objeto_Perdido import ObjetoPerdido 
from app.Modelo.Usuario import Usuario
from app.Modelo.Carrera import Carrera

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial', methods=['GET'])
@login_required
def historial():
    try:
        
        historial_objetos = db.session.query(
            Historial,
            ObjetoPerdido.nombre_objeto,
            ObjetoPerdido.foto,
            ObjetoPerdido.sala_encontrada,
            ObjetoPerdido.hora_encontrada,
            Usuario.nombre_completo,
        ) \
        .join(ObjetoPerdido, Historial.id_objeto == ObjetoPerdido.id_objeto) \
        .outerjoin(Usuario, Historial.entregado_a == Usuario.rut) \
        .filter(ObjetoPerdido.activo == False) \
        .all()

        return render_template('historial.html', historial=historial_objetos)
    except Exception as e:
        print(f"Error al cargar el historial: {e}")
        flash('Ocurrió un error al cargar el historial.', 'error')
        return redirect(url_for('auth.home_admin'))


