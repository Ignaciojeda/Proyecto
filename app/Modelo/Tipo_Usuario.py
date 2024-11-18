from app import db

class TipoUsuario(db.Model):
    __tablename__ = 'Tipo_usuario' 

    id_tipo_usuario = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    

    usuarios = db.relationship('Usuario', back_populates='tipo_usuario')


