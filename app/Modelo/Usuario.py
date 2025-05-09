from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'Usuario'  

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellido = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    telefono = db.Column(db.String(45))
    password = db.Column(db.String(255), nullable=False)  
    tipoUsuario = db.Column(db.Integer, db.ForeignKey('TIPO_USUARIO.idTipoUsuario'), nullable=False)
    
    # Relaciones usando strings
    tipo = db.relationship('TipoUsuario', back_populates='usuarios')
    pedidos = db.relationship('Pedido', back_populates='cliente', lazy='dynamic')

    def __init__(self, nombre, apellido, email, telefono, password, tipoUsuario):
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