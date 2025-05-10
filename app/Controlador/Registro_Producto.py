from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.Modelo.Producto import Producto
from app.Modelo.Marca import Marca
from app.Modelo.Categoria import Categoria
from app import db
import os
from werkzeug.utils import secure_filename

producto_bp = Blueprint('producto', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@producto_bp.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@login_required
def registrar_producto():
    if current_user.tipoUsuario != 1:  # Solo admin
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('home'))
    
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio'))
        marca_id = int(request.form.get('marca'))
        categoria_id = int(request.form.get('categoria'))
        
        # Manejo de la imagen
        imagen = request.files.get('imagen')
        imagen_nombre = None
        
        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join('app/static/img/productos', filename))
            imagen_nombre = filename
        
        nuevo_producto = Producto(
            nombreProducto=nombre,
            descripcion=descripcion,
            precio=precio,
            marcaId=marca_id,
            categoriaId=categoria_id,
            imagen=imagen_nombre
        )
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        flash('Producto registrado exitosamente', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('registro_producto.html', 
                         marcas=marcas, 
                         categorias=categorias)