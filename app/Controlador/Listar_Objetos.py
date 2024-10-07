from flask import Blueprint, render_template
from app.Modelo.Objeto_Perdido import ObjetoPerdido

listar_bp = Blueprint('listar', __name__)

@listar_bp.route('/objeto_perdido')
def lista_objetos():
    objetos = ObjetoPerdido.query.all()
    return render_template('templates/listar_objetos.html', objetos=objetos)
