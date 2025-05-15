from app import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = 'PEDIDO' 

    idPedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clienteId = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'), nullable=False)
    fechaPedido = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    direccionEnvio = db.Column(db.String(100), nullable=False)
    sucursalID = db.Column(db.Integer, db.ForeignKey('SUCURSAL.sucursalId'))
    etapaId = db.Column(db.Integer, db.ForeignKey('ETAPA_PEDIDO.idEtapaPedido'), default=1)

    # Relaciones usando strings
    cliente = db.relationship('Usuario', back_populates='pedidos')
    sucursal = db.relationship('Sucursal', back_populates='pedidos')
    etapa = db.relationship('EtapaPedido', back_populates='pedidos')
    detalles = db.relationship('DetallePedido', back_populates='pedido', cascade='all, delete-orphan')


    def __init__(self, clienteId, total, direccionEnvio, sucursalID=None, etapaId=1):
        self.clienteId = clienteId
        self.total = total
        self.direccionEnvio = direccionEnvio
        self.sucursalID = sucursalID
        self.etapaId = etapaId

    def __repr__(self):
        return f'<Pedido {self.idPedido}>'