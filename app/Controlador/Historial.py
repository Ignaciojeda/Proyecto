from flask import Blueprint, render_template
from app import db
from app.Modelo.Objeto_Perdido import ObjetoPerdido  
from flask_login import login_required

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial', methods=['GET'])
@login_required
def historial():

    objetos_subidos = ObjetoPerdido.query.all()

    return render_template('Historial.html', objetos_subidos=objetos_subidos)