from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.Modelo.Objeto_Perdido import ObjetoPerdido

listara_bp = Blueprint('listara', __name__)

@listara_bp.route('/listar_objeto_admin')
@login_required
def lista_objetos_admin():
    # Verifica si el usuario es administrador
    if current_user.tipo_usuario.descripcion != 'Admin':
        abort(403)  # Permiso denegado
    objetos = ObjetoPerdido.query.filter_by(activo=True).all()
    print(f"Objetos encontrados: {len(objetos)}")  
    return render_template('Listar_Objeto_Admin.html', objetos=objetos)
