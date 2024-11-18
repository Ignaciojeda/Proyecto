from app import db
from flask_login import UserMixin
from app.Modelo.Tipo_Usuario import TipoUsuario
from app.Modelo.Carrera import Carrera
from werkzeug.security import generate_password_hash, check_password_hash  

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    
    rut = db.Column(db.String(10), primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey('Carrera.id_carrera'))
    correo = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(255), nullable=False)
    tipo_usuario_id = db.Column(db.Integer, db.ForeignKey('Tipo_usuario.id_tipo_usuario'), nullable=False)

    tipo_usuario  = db.relationship('TipoUsuario', back_populates='usuarios', lazy=True)
    carrera = db.relationship('Carrera', back_populates='usuarios')
    objetos_perdidos = db.relationship('ObjetoPerdido', back_populates='usuario', cascade='all, delete-orphan', lazy=True)
    historial = db.relationship('Historial', back_populates='usuario')

    def __init__(self, rut, nombre_completo, carrera, correo, contraseña, tipo_usuario):
        self.rut = rut
        self.nombre_completo = nombre_completo
        self.carrera = carrera
        self.correo = correo
        self.set_password(contraseña)
        self.tipo_usuario = tipo_usuario

    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)

    def get_id(self):
        return self.rut
    
    def __repr__(self):
        return f'<Usuario {self.correo}>'
