from flask import Blueprint, render_template
from app.Modelo.Objeto_Perdido import ObjetoPerdido

listar_bp = Blueprint('listar', __name__)

@listar_bp.route('/listar_objeto')
def lista_objetos():
    objetos = ObjetoPerdido.query.all()
    print(f"Objetos encontrados: {len(objetos)}")  
    return render_template('Listar_Objeto.html', objetos=objetos)