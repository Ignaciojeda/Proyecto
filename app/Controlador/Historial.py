from flask import Blueprint, render_template, request, redirect, url_for,flash
from app import db
from app.Modelo.Objeto_Perdido import ObjetoPerdido  

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial', methods=['GET'])
def historial():
    objetos_perdidos = ObjetoPerdido.query.filter_by(activo=False).order_by(ObjetoPerdido.fecha_creacion.desc()).all()
    objetos_subidos = ObjetoPerdido.query.filter_by(activo=True).order_by(ObjetoPerdido.fecha_creacion.desc()).all()
    
    return render_template('historial.html', objetos_perdidos=objetos_perdidos, objetos_subidos=objetos_subidos)