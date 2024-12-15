from app import db
from datetime import datetime, time

class Historial(db.Model):
    __tablename__ = 'Historial'

    id_historial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_objeto = db.Column(db.Integer, db.ForeignKey('Objetos_Perdidos.id_objeto'), nullable=False)
    rut_usuario = db.Column(db.String(12), db.ForeignKey('Usuario.rut'), nullable=False)  # Usar db.String(12) para coincidir con Usuario
    sala_encontrada = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255))
    fecha_accion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    entregado_a = db.Column(db.String(100))

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='historial_recibidos', lazy=True)
    objeto = db.relationship('ObjetoPerdido', back_populates='historial_objetos')

    def __init__(self, id_objeto, rut_usuario, sala_encontrada, descripcion, activo=True, entregado_a=None, hora_entrega=None):
        self.id_objeto = id_objeto
        self.rut_usuario = rut_usuario
        self.sala_encontrada = sala_encontrada
        self.descripcion = descripcion
        self.activo = activo
        self.entregado_a = entregado_a
        self.hora_entrega = hora_entrega
