from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'

    id_tipo_usuario = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(45), nullable=False)


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id_tipo_usuario'), nullable=False)
    correo_usuario = db.Column(db.String(45), nullable=False, unique=True)
    contraseña = db.Column(db.String(128), nullable=False)

    tipo_usuario = db.relationship('TipoUsuario', backref='usuarios')

    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)