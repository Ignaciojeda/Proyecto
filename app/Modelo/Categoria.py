from app import db

class Categoria(db.Model):
    __tablename__ = 'CATEGORIA'

    categoriaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45), nullable=False)
    descripcion = db.Column(db.String(45))

    productos = db.relationship('Producto', back_populates='categoria')

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f'<Categoria {self.nombre}>'
