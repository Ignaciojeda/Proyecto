from app import db

class Inventario(db.Model):
    __tablename__ = 'INVENTARIO'

    sucursal_id = db.Column(db.Integer, db.ForeignKey('SUCURSAL.sucursalId'), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('PRODUCTO.idProducto'), primary_key=True)
    stock = db.Column(db.Integer, nullable=False)

    sucursal = db.relationship('Sucursal', back_populates='inventarios')
    producto = db.relationship('Producto', back_populates='inventarios')

    def __repr__(self):
        return f'<Inventario sucursal_id={self.sucursal_id}, producto_id={self.producto_id}>'