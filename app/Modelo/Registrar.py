from app import db


class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'

    id_tipo_usuario = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(45), nullable=False)

    def __init__(self, id_tipo_usuario, descripcion):
        self.id_tipo_usuario = id_tipo_usuario
        self.descripcion = descripcion

        
class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id_tipo_usuario'), nullable=False)
    correo_usuario = db.Column(db.String(45), nullable=False)
    contraseña = db.Column(db.String(45), nullable=False)  

    def __init__(self, id_usuario, id_tipo_usuario, correo_usuario, contraseña):
        self.id_usuario = id_usuario
        self.id_tipo_usuario = id_tipo_usuario
        self.correo_usuario = correo_usuario
        self.contraseña = contraseña

    tipo_usuario = db.relationship('TipoUsuario', backref=db.backref('usuario', lazy=True))