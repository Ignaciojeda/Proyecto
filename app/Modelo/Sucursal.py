from app import db

class Sucursal(db.Model):
    __tablename__ = 'SUCURSAL'

    sucursalId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    direccion = db.Column(db.String(45))
    region = db.Column(db.String(45))
    comuna = db.Column(db.String(45))
    
    pedidos = db.relationship('Pedido', back_populates='sucursal')



    def __init__(self, sucursalId ,nombre, direccion, region):
        self.sucursalId = sucursalId
        self.nombre =  nombre
        self.direccion = direccion
        self.region = region
        

    def __repr__(self):
        return f'<Sucursal {self.nombre}>'
