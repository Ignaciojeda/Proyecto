from app import db
from datetime import datetime

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=False)
    usuario = db.Column(db.String(120), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)  # Valor entre 1 y 5
    fecha = db.Column(db.DateTime, default=datetime.utcnow)