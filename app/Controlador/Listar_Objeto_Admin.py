from flask import Blueprint, render_template, abort, request, url_for, flash, redirect
from flask_login import login_required, current_user
from app.Modelo.Objeto_Perdido import ObjetoPerdido
from app.Modelo.Historial import Historial
from app import db

listara_bp = Blueprint('listara', __name__)

@listara_bp.route('/listar_objeto_admin')
@login_required
def lista_objetos_admin():
    if current_user.tipo_usuario.descripcion != 'Admin':
        abort(403)  # Permiso denegado
    objetos = ObjetoPerdido.query.filter_by(activo=True).all()
    print(f"Objetos encontrados: {len(objetos)}")  
    return render_template('Listar_Objeto_Admin.html', objetos=objetos)

@listara_bp.route('/entregar_objeto/<int:id>', methods=['POST'])
def entregar_objeto(id):
    objeto = ObjetoPerdido.query.get_or_404(id)
    return render_template('entregar_objeto.html', objeto=objeto)

@listara_bp.route('/entregar/<int:id>', methods=['POST'])
@login_required
def entregar(id):
    objeto = ObjetoPerdido.query.get_or_404(id)

    # Capturar datos del formulario
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    carrera = request.form.get('carrera')

    if not all([nombre, correo, carrera]):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('listara.entregar_objeto', id=id))

    # Crear un nuevo historial de entrega
    entrega = Historial(nombre=nombre, correo=correo, carrera=carrera, objeto_id=objeto.id)
    db.session.add(entrega)

    # Marcar el objeto como no activo (oculto)
    objeto.activo = False
    db.session.commit()

    flash('El objeto ha sido entregado correctamente.', 'success')
    return redirect(url_for('listara.lista_objetos_admin'))