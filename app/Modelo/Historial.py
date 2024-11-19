from app import db
from datetime import datetime

class Historial(db.Model):
    __tablename__ = 'Historial'

    id_historial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_objeto = db.Column(db.Integer, db.ForeignKey('Objetos_Perdidos.id_objeto'), nullable=False)
    rut_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.rut'), nullable=False)  # Rut del usuario que subió el objeto
    sala_encontrada = db.Column(db.String(50), nullable=False)  # Sala donde se encontró el objeto
    descripcion = db.Column(db.String(255))  # Descripción del objeto
    fecha_accion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    entregado_a = db.Column(db.String(100))  # Persona a quien se entregó el objeto (opcional)

    usuario = db.relationship('Usuario', backref='historiales', lazy=True)
    objeto = db.relationship('ObjetoPerdido', backref='historial_objetos', lazy=True)

    def __init__(self, id_objeto, rut_usuario, sala_encontrada, descripcion, activo=True, entregado_a=None):
        self.id_objeto = id_objeto
        self.rut_usuario = rut_usuario
        self.sala_encontrada = sala_encontrada
        self.descripcion = descripcion
        self.activo = activo
        self.entregado_a = entregado_a
