from app import db
from flask_login import UserMixin
from app.Modelo.Tipo_Usuario import TipoUsuario
from app.Modelo.Carrera import Carrera
from werkzeug.security import generate_password_hash, check_password_hash  

class Usuario(db.Model):
    __tablename__ = 'Usuario'  # Nombre de la tabla en mayúsculas

    
    rut = db.Column(db.String(12), primary_key=True)  # rut es la clave primaria
    nombre_completo = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.Integer, db.ForeignKey('Carrera.id_carrera'), nullable=False)  # Aquí también se usa el nombre correcto de la tabla en mayúsculas
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.Integer, db.ForeignKey('Tipo_usuario.id_tipo_usuario'), nullable=False)
    
    # Relaciones
    carrera_relacion = db.relationship('Carrera', back_populates='usuarios')
    tipo_usuario_relacion = db.relationship('TipoUsuario', back_populates='usuarios')
    objetos_perdidos = db.relationship('ObjetoPerdido', back_populates='usuario', lazy=True)
    historial_recibidos = db.relationship('Historial', backref='historiales', lazy=True) 

    def is_active(self):
        return True     
    
    def is_authenticated(self):
        return True  

    def is_anonymous(self):
        return False


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
