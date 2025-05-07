from app import db

class Marca(db.Model):
    __tablename__ = 'MARCA'

    marcaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreMarca = db.Column(db.String(45), nullable=False)
    descripcion = db.Column(db.String(45))

    productos = db.relationship('Producto', back_populates='marca')

    def __init__(self, nombreMarca, descripcion):
        self.nombreMarca = nombreMarca
        self.descripcion = descripcion

    def __repr__(self):
        return f'<Marca {self.nombreMarca}>'
