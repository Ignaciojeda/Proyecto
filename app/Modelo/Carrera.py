from app import db

class Carrera(db.Model):
    __tablename__ = 'Carrera'
    
    id_carrera = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)

    usuarios = db.relationship('Usuario', back_populates='carrera_relacion', lazy=True)
