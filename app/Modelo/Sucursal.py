from app import db

class Sucursal(db.Model):
    __tablename__ = 'SUCURSAL'

    sucursalId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    direccion = db.Column(db.String(45))
    region = db.Column(db.String(45))
    comuna = db.Column(db.String(45))
    
    # Relaciones
    pedidos = db.relationship('Pedido', back_populates='sucursal')
    inventarios = db.relationship('Inventario', back_populates='sucursal')

    def __repr__(self):
        return f'<Sucursal {self.nombre}>'