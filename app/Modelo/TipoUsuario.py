from app import db

class TipoUsuario(db.Model):
    __tablename__ = 'TIPO_USUARIO'

    idTipoUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(45), nullable=False)

    usuarios = db.relationship('Usuario', back_populates='tipo')

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return f'<TipoUsuario {self.descripcion}>'
