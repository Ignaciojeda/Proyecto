from app import db
from datetime import datetime
import pytz

chile_tz = pytz.timezone('Chile/Continental')

class ObjetoPerdido(db.Model):
    __tablename__ = 'Objetos_Perdidos'  # Nombre de la tabla en la base de datos

    id_objeto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_objeto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    foto = db.Column(db.LargeBinary)
    sala_encontrada = db.Column(db.String(50), nullable=False)
    hora_encontrada = db.Column(db.Time, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    rut_usuario = db.Column(db.String(10), db.ForeignKey('Usuario.rut'), nullable=False)

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='objetos_perdidos', lazy=True)
    historial_objetos = db.relationship('Historial', back_populates='objeto', lazy=True)

    def __repr__(self):
        return f'<ObjetoPerdido {self.nombre_objeto}>'

    def __init__(self, nombre_objeto, sala_encontrada, hora_encontrada, rut_usuario, descripcion=None, foto=None, activo=True):
        self.nombre_objeto = nombre_objeto
        self.descripcion = descripcion
        self.foto = foto
        self.sala_encontrada = sala_encontrada
        self.hora_encontrada = hora_encontrada
        self.activo = activo
        self.rut_usuario = rut_usuario
