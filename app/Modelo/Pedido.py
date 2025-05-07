from app import db
from app.Modelo.Cliente import Cliente
from app.Modelo.Sucursal import Sucursal
from app.Modelo.EtapaPedido import EtapaPedido

class Pedido(db.Model):
    __tablename__ = 'PEDIDO'

    idPedido = db.Column(db.Integer, primary_key=True)
    clienteId = db.Column(db.Integer, db.ForeignKey('CLIENTE.IdCliente'), nullable=False)
    fechaPedido = db.Column(db.Date)
    total = db.Column(db.Integer)
    direccionEnvio = db.Column(db.String(45))
    sucursalID = db.Column(db.Integer, db.ForeignKey('SUCURSAL.sucursalId'))
    etapaId = db.Column(db.Integer, db.ForeignKey('ETAPA_PEDIDO.idEtapaPedido'))

    cliente = db.relationship('Cliente', back_populates='pedidos')
    sucursal = db.relationship('Sucursal', back_populates='pedidos')
    etapa = db.relationship('EtapaPedido', back_populates='pedidos')

    def __init__(self, clienteId, fechaPedido, total, direccionEnvio, sucursalID, etapaId):
        self.clienteId = clienteId
        self.fechaPedido = fechaPedido
        self.total = total
        self.direccionEnvio = direccionEnvio
        self.sucursalID = sucursalID
        self.etapaId = etapaId

    def __repr__(self):
        return f'<Pedido {self.idPedido} - Cliente {self.clienteId}>'
