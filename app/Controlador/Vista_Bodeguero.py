from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.Modelo.Inventario import Inventario
from app.Modelo.Sucursal import Sucursal

bodeguero_bp = Blueprint('bodeguero', __name__)

@bodeguero_bp.route('/bodeguero')
@login_required
def dashboard():
    if current_user.tipoUsuario != 3:  # Asumiendo que 3 es el ID para bodegueros
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('home'))
    
    sucursal = Sucursal.query.filter_by(encargadoId=current_user.idUsuario).first()
    
    if not sucursal:
        flash('No tienes una sucursal asignada', 'error')
        return redirect(url_for('home'))
    
    inventario = Inventario.query.filter_by(sucursal_id=sucursal.sucursalId).all()
    
    return render_template('vista_bodeguero.html', 
                         sucursal=sucursal, 
                         inventario=inventario)