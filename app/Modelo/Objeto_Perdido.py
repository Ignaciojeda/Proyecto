from app import db
from datetime import datetime
import pytz

chile_tz = pytz.timezone('Chile/Continental')

class ObjetoPerdido(db.Model):
    __tablename__ = 'Objetos_Perdidos'  # Asegúrate de que coincide con el nombre en tu base de datos

    id_objeto = db.Column(db.Integer, primary_key=True)
    nombre_objeto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    foto = db.Column(db.Text, nullable=True)  
    sala_encontrada = db.Column(db.String(50), nullable=False)
    hora_encontrada = db.Column(db.Time, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    rut_usuario = db.Column(db.String(10), db.ForeignKey('Usuario.rut'), nullable=False)  # Ajusta al nombre real de la tabla y columna

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='objetos_perdidos', lazy=True)
    historial = db.relationship('Historial', back_populates='objeto', cascade='all, delete-orphan', lazy=True)

    def __init__(self, nombre_objeto, sala_encontrada, hora_encontrada, descripcion=None, foto=None, activo=True):
        self.nombre_objeto = nombre_objeto
        self.descripcion = descripcion
        self.foto = foto
        self.sala_encontrada = sala_encontrada
        self.hora_encontrada = hora_encontrada
        self.activo = activo

    def __repr__(self):
        return f'<ObjetoPerdido {self.nombre_objeto}>'
