from app import db

class EtapaPedido(db.Model):
    __tablename__ = 'ETAPA_PEDIDO'

    idEtapaPedido = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(45))
                            
    pedidos = db.relationship('Pedido', back_populates='etapa')

    
    def __init__(self, idEtapaPedido , descripcion):
        self.idEtapaPedido = idEtapaPedido
        self.descripcion = descripcion

    def __repr__(self):
        return f'<EtapaPedido {self.descripcion}>'
