from app import db
from app import current_app
from app.Services.Conversor_Divisas import ServicioDivisas

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
    detalles = db.relationship('DetallePedido', back_populates='producto')
    comentarios = db.relationship('Comentario', back_populates='producto', lazy='dynamic')


    def __repr__(self):
        return f'<Producto {self.nombreProducto}>'
    
    def precio_en_divisa(self, moneda='USD'):
        """Devuelve el precio convertido a otra moneda"""
        precio_local = self.precio_actual()
        if moneda.upper() == current_app.config['MONEDA_LOCAL']:
            return precio_local
        
        return ServicioDivisas.convertir(
            precio_local,
            current_app.config['MONEDA_LOCAL'],
            moneda.upper()
        )
    
    def to_dict(self, detallado=False, moneda=None):
        data = {
            # ... (campos existentes)
            'precio_actual': self.precio_actual(),
        }
        
        if moneda and moneda.upper() in current_app.config['MONEDAS_SOPORTADAS']:
            precio_convertido = self.precio_en_divisa(moneda)
            data['precio_convertido'] = {
                'moneda': moneda.upper(),
                'valor': round(precio_convertido, 2),
                'tasa_cambio': ServicioDivisas.obtener_tasa_actual(moneda.upper())
            }
        
        return data