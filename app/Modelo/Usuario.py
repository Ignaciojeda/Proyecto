from app import db
from flask_login import UserMixin
from app.Modelo.Tipo_Usuario import TipoUsuario

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id_tipo_usuario'), nullable=False)
    correo_usuario = db.Column(db.String(45), nullable=False, unique=True)
    contraseña = db.Column(db.String(255), nullable=False)  # Almacena la contraseña sin hash

    tipo_usuario = db.relationship('TipoUsuario', back_populates='usuarios', lazy=True)  # Usar back_populates

    def set_password(self, password):
        self.contraseña = password  # Almacenar la contraseña directamente

    def check_password(self, password):
        return self.contraseña == password  # Comparar directamente las contraseñas

    def get_id(self):
        return str(self.id_usuario)
    
    def __repr__(self):
        return f'<Usuario {self.correo_usuario}>'
