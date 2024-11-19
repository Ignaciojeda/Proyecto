from app import db

class Carrera(db.Model):
    __tablename__ = 'Carrera'  # Nombre tal como está en la base de datos
    
    id_carrera = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)

    # Relación con Usuario
    usuarios = db.relationship('Usuario', back_populates='carrera_relacion')
