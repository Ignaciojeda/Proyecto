from flask import Blueprint, render_template
from app.Modelo.Objeto_Perdido import ObjetoPerdido
from flask_login import login_required

listar_bp = Blueprint('listar', __name__)

@listar_bp.route('/listar_objeto')
@login_required
def lista_objetos():
    objetos = ObjetoPerdido.query.filter_by(activo=True).all()
    print(f"Objetos encontrados: {len(objetos)}")  
    return render_template('Listar_Objeto.html', objetos=objetos)
