from app import db

class Producto(db.Model):
    __tablename__ = 'PRODUCTO'

    idProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreProducto = db.Column(db.String(45), nullable=False)
    descripcion = db.Column(db.String(45))
    precio = db.Column(db.Integer)
    marcaId = db.Column(db.Integer, db.ForeignKey('MARCA.marcaId'), nullable=False)
    categoriaId = db.Column(db.Integer, db.ForeignKey('CATEGORIA.categoriaId'), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)
    stock = db.Column(db.Integer, nullable=False)

    marca = db.relationship('Marca', back_populates='productos')
    categoria = db.relationship('Categoria', back_populates='productos')
    inventarios = db.relationship('Inventario', back_populates='producto')
    carrito = db.relationship('Carrito', back_populates='producto')

    def __repr__(self):
        return f'<Producto {self.nombreProducto}>'