from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.Modelo.TipoUsuario import TipoUsuario 

class Usuario(db.Model):
    __tablename__ = 'Usuario'

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45))
    apellido = db.Column(db.String(45))
    email = db.Column(db.String(45))
    telefono = db.Column(db.String(45))
    password = db.Column(db.String(50)) 
    tipoUsuario = db.Column(db.Integer, db.ForeignKey('TIPO_USUARIO.idTipoUsuario'), nullable=False)
    
    pedido = db.relationship('Pedido', back_populates='cliente')
    tipo = db.relationship('TipoUsuario', back_populates='usuarios')

    def __init__(self, idUsuario, nombre, apellido, email, telefono, password, tipoUsuario):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.set_password(password)
        self.tipoUsuario = tipoUsuario

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Usuario {self.email}>'
