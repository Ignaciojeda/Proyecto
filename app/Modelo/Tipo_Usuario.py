from app import db

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    __table_args__ = {'extend_existing': True}  

    id_tipo_usuario = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)

    
    usuarios = db.relationship('Usuario', back_populates='tipo_usuario', lazy=True)

    def __repr__(self):
        return f'<TipoUsuario {self.descripcion}>'
