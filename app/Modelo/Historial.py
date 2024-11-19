from app import db

class Historial(db.Model):
    __tablename__ = 'Historial' 
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100), nullable=False)
    objeto_id = db.Column(db.Integer, db.ForeignKey('Objetos_Perdidos.id_objeto'), nullable=False) 
    usuario_rut = db.Column(db.String(10), db.ForeignKey('Usuario.rut'), nullable=False)  
    
    # Relaciones
    objeto = db.relationship('ObjetoPerdido', back_populates='historial')  
    usuario = db.relationship('Usuario', back_populates='historial')  
