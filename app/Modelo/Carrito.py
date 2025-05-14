from app import db

class Carrito(db.Model):
    __tablename__ = 'CARRITO'

    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'), primary_key=True)
    productoId = db.Column(db.Integer, db.ForeignKey('PRODUCTO.idProducto'), primary_key=True)
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)

    producto = db.relationship('Producto', back_populates='carrito')
    usuario = db.relationship('Usuario', back_populates='carrito')

    def __init__(self, usuarioId, productoId, cantidad, precio):
        self.usuarioId = usuarioId
        self.productoId = productoId
        self.cantidad = cantidad
        self.precio = precio
   

def __repr__(self):
    return f'<Carrito usuarioId={self.usuarioId}, productoId={self.productoId}, cantidad={self.cantidad}, precio={self.precio}>'
