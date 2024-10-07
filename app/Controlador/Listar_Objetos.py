from flask import Blueprint, render_template
from app.Modelo.Objeto_Perdido import ObjetoPerdido

# Blueprint para listar los objetos
listar_bp = Blueprint('listar', __name__)

@listar_bp.route('/objetos_perdidos')
def lista_objetos():
    objetos = ObjetoPerdido.query.all()
    return render_template('../Templates/Listar_Objetos.html', objetos=objetos)
