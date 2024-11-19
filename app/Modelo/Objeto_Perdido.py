from app import db
from datetime import datetime
import pytz

chile_tz = pytz.timezone('Chile/Continental')

class ObjetoPerdido(db.Model):
    __tablename__ = 'Objetos_Perdidos'  # Asegúrate de que coincide con el nombre en tu base de datos

    # Columnas
    id_objeto = db.Column(db.Integer, primary_key=True)  # Clave primaria del objeto
    nombre_objeto = db.Column(db.String(100), nullable=False)  # Nombre del objeto
    descripcion = db.Column(db.Text, nullable=True)  # Descripción del objeto
    foto = db.Column(db.Text, nullable=True)  # Foto del objeto (URL o path)
    sala_encontrada = db.Column(db.String(50), nullable=False)  # Sala donde se encontró el objeto
    hora_encontrada = db.Column(db.DateTime, nullable=False)  # Fecha y hora en que se encontró el objeto
    activo = db.Column(db.Boolean, default=True)  # Estado del objeto, activo por defecto
    rut_usuario = db.Column(db.String(12), db.ForeignKey('Usuario.rut'), nullable=False)  # Rut del usuario que sube el objeto

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='objetos_perdidos', lazy=True)  # Relación con Usuario
    historial = db.relationship('Historial', back_populates='objeto', cascade='all, delete-orphan', lazy=True)  # Relación con Historial

    def __init__(self, nombre_objeto, sala_encontrada, hora_encontrada, descripcion=None, foto=None, activo=True):
        self.nombre_objeto = nombre_objeto
        self.descripcion = descripcion
        self.foto = foto
        self.sala_encontrada = sala_encontrada
        self.hora_encontrada = hora_encontrada
        self.activo = activo

    def __repr__(self):
        return f'<ObjetoPerdido {self.nombre_objeto}>'
