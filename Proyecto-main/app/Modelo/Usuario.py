from app import db
from flask_login import UserMixin
from app.Modelo.Tipo_Usuario import TipoUsuario
from werkzeug.security import generate_password_hash, check_password_hash  

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id_tipo_usuario'), nullable=False)
    correo_usuario = db.Column(db.String(45), nullable=False, unique=True)
    contraseña = db.Column(db.String(255), nullable=False)

    tipo_usuario = db.relationship('TipoUsuario', back_populates='usuarios', lazy=True)  

    def __init__(self, id_tipo_usuario, correo_usuario, contraseña):
        self.id_tipo_usuario = id_tipo_usuario
        self.correo_usuario = correo_usuario
        self.set_password(contraseña) 

    def set_password(self, password):
       
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
      
        return check_password_hash(self.contraseña, password)

    def get_id(self):
        return str(self.id_usuario)
    
    def __repr__(self):
        return f'<Usuario {self.correo_usuario}>'
