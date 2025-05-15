from app import db


class DetallePedido(db.Model):
    __tablename__ = 'DETALLE_PEDIDO'

    idDetalle = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pedidoId = db.Column(db.Integer, db.ForeignKey('PEDIDO.idPedido'), nullable=False)
    productoId = db.Column(db.Integer, db.ForeignKey('PRODUCTO.idProducto'), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Integer, nullable=False) 

    pedido = db.relationship('Pedido', back_populates='detalles')
    producto = db.relationship('Producto', back_populates='detalles')
