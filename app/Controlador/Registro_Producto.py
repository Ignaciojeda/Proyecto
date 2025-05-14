from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, send_file
from flask_login import login_required, current_user
from app.Modelo.Producto import Producto
from app.Modelo.Marca import Marca
from app.Modelo.Categoria import Categoria
from app import db
import os,io
from werkzeug.utils import secure_filename

producto_bp = Blueprint('producto', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB máximo

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@producto_bp.route('', methods=['GET', 'POST'])
@login_required
def registrar_producto():
    # Verificación de permisos
    if current_user.tipoUsuario ==1: 
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('home.home'))
    
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    
    if request.method == 'POST':
        try:
            # Obtención de datos del formulario
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            precio = int(request.form.get('precio'))  # Cambiado a int según modelo
            marca_id = int(request.form.get('marca'))
            categoria_id = int(request.form.get('categoria'))
            
            # Manejo de la imagen como LargeBinary
            imagen = request.files.get('imagen')
            imagen_data = None
            
            if imagen and imagen.filename != '':
                # Validación de tamaño de imagen
                if len(imagen.read()) > MAX_IMAGE_SIZE:
                    flash('La imagen es demasiado grande. Tamaño máximo: 2 MB.', 'error')
                    return redirect(url_for('producto.registrar_producto'))
                
                imagen.seek(0)  # Resetear el puntero del archivo
                
                if allowed_file(imagen.filename):
                    imagen_data = imagen.read()  # Leer los bytes de la imagen
                else:
                    flash('Formato de imagen no permitido. Use JPG, PNG o JPEG.', 'error')
                    return redirect(url_for('producto.registrar_producto'))
            else:
                flash('Debe seleccionar una imagen para el producto', 'error')
                return redirect(url_for('producto.registrar_producto'))
            
            # Creación del nuevo producto
            nuevo_producto = Producto(
                nombreProducto=nombre,
                descripcion=descripcion,
                precio=precio,
                marcaId=marca_id,
                categoriaId=categoria_id,
                imagen=imagen_data  # Guardamos los bytes directamente
            )
            
            db.session.add(nuevo_producto)
            db.session.commit()
            
            flash('Producto registrado exitosamente', 'success')
            return redirect(url_for('admin.dashboard'))
            
        except ValueError as ve:
            db.session.rollback()
            flash(f'Error en los datos numéricos: {str(ve)}', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al registrar el producto: {str(e)}', 'error')
    
    return render_template('registro_producto.html', 
                         marcas=marcas, 
                         categorias=categorias)


