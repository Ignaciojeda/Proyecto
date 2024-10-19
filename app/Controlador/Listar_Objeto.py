from flask import Blueprint, render_template,session,redirect,url_for
from app.Modelo.Objeto_Perdido import ObjetoPerdido

listar_bp = Blueprint('listar', __name__)

@listar_bp.route('/listar_objeto')
def lista_objetos():

    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['usuario_rol'] == 'estudiante':
        objetos = ObjetoPerdido.query.with_entities(ObjetoPerdido.nombre, ObjetoPerdido.descripcion, ObjetoPerdido.foto).all()
    else:
        objetos = ObjetoPerdido.query.all()

    return render_template('Listar_Objeto.html', objetos=objetos)
