from app import db

class Historial(db.Model):
    __tablename__ = 'historial'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100), nullable=False)
    objeto_id = db.Column(db.Integer, db.ForeignKey('objetos_perdidos.id_objeto'), nullable=False)
    
    # Relación con ObjetoPerdido
    objeto = db.relationship('ObjetoPerdido', back_populates='historial')
    usuario_rut = db.Column(db.Integer, db.ForeignKey('usuario.rut'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='historial')

