from app import db
from app.Modelo.Producto import Producto
from app.Modelo.Sucursal import Sucursal

class Inventario(db.Model):
    __tablename__ = 'INVENTARIO'

    sucursal_id = db.Column(db.Integer, db.ForeignKey('SUCURSAL.sucursalId'), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('PRODUCTO.idProducto'), primary_key=True)
    stock = db.Column(db.Integer, nullable=False)

    sucursal = db.relationship('Sucursal', back_populates='inventarios')
    producto = db.relationship('Producto', back_populates='inventarios')

    def __init__(self, sucursal_id, producto_id, stock):
        self.sucursal_id = sucursal_id
        self.producto_id = producto_id
        self.stock = stock

    def __repr__(self):
        return f'<Inventario sucursal_id={self.sucursal_id}, producto_id={self.producto_id}, stock={self.stock}>'
