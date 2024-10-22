from app import db
from datetime import datetime
import pytz

# Define la zona horaria UTC-3 (por ejemplo, Santiago, Chile)
chile_tz = pytz.timezone('Chile/Continental')

class ObjetoPerdido(db.Model):
    __tablename__ = 'objetos_perdidos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    foto = db.Column(db.LargeBinary, nullable=True)  
    sala_encontrada = db.Column(db.String(100), nullable=False)
    hora_encontrada = db.Column(db.Time, nullable=False)
    fecha_encontrada = db.Column(db.Date, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(chile_tz))

    def __init__(self, nombre, descripcion=None, foto=None, sala_encontrada='', hora_encontrada=None, fecha_encontrada=None, fecha_creacion=None, activo=True):
        self.nombre = nombre
        self.descripcion = descripcion
        self.foto = foto
        self.sala_encontrada = sala_encontrada
        self.hora_encontrada = hora_encontrada
        self.fecha_encontrada = fecha_encontrada
        self.activo = activo
        self.fecha_creacion = datetime.now(chile_tz)
