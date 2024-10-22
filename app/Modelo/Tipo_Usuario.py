from app import db

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    
    id_tipo_usuario = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)

    # Relación inversa con Usuario usando back_populates
    usuarios = db.relationship('Usuario', back_populates='tipo_usuario', lazy=True)

    def __repr__(self):
        return f'<TipoUsuario {self.descripcion}>'
