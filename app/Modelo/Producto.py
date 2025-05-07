from app import db
from app.Modelo.Marca import Marca
from app.Modelo.Categoria import Categoria
from app.Modelo.Inventario import Inventario

class Producto(db.Model):
    __tablename__ = 'PRODUCTO'

    idProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreProducto = db.Column(db.String(45), nullable=False)
    descripcion = db.Column(db.String(45))
    precio = db.Column(db.Integer)
    marcaId = db.Column(db.Integer, db.ForeignKey('MARCA.marcaId'), nullable=False)
    categoriaId = db.Column(db.Integer, db.ForeignKey('CATEGORIA.categoriaId'), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)

    marca = db.relationship('Marca', back_populates='productos')
    categoria = db.relationship('Categoria', back_populates='productos')
    inventarios = db.relationship('Inventario', back_populates='producto')

    def __init__(self, nombreProducto, descripcion, precio, marcaId, categoriaId, imagen):
        self.nombreProducto = nombreProducto
        self.descripcion = descripcion
        self.precio = precio
        self.marcaId = marcaId
        self.categoriaId = categoriaId
        self.imagen = imagen

    def __repr__(self):
        return f'<Producto {self.nombreProducto}>'
