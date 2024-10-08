from app import db

class ObjetoPerdido(db.Model):
    __tablename__ = 'objetos_perdidos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    foto = db.Column(db.LargeBinary, nullable=True)  
    sala_encontrada = db.Column(db.String(100), nullable=False)
    hora_encontrada = db.Column(db.Time, nullable=False)
    fecha_encontrada = db.Column(db.Date, nullable=False)

    def __init__(self, nombre, descripcion, foto, sala_encontrada, hora_encontrada, fecha_encontrada):
        self.nombre = nombre
        self.descripcion = descripcion
        self.foto = foto
        self.sala_encontrada = sala_encontrada
        self.hora_encontrada = hora_encontrada
        self.fecha_encontrada = fecha_encontrada
