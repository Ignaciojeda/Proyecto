from app import db

class Producto(db.Model):
    __tablename__ = 'PRODUCTO'

    idProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreProducto = db.Column(db.String(45), nullable=False)
    descripcion = db.Column(db.String(45))
    precio = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)  # Nuevo campo
    marcaId = db.Column(db.Integer, db.ForeignKey('MARCA.marcaId'), nullable=False)
    categoriaId = db.Column(db.Integer, db.ForeignKey('CATEGORIA.categoriaId'), nullable=False)
    imagen = db.Column(db.LargeBinary)

    # Relaciones
    marca = db.relationship('Marca', back_populates='productos')
    categoria = db.relationship('Categoria', back_populates='productos')
    inventarios = db.relationship('Inventario', back_populates='producto')

    def __repr__(self):
        return f'<Producto {self.nombreProducto}>'
    
    def actualizar_stock(self, cantidad):
        """Método para actualizar el stock"""
        self.stock += cantidad
        db.session.commit()
    
    def tiene_stock(self, cantidad):
        """Verifica si hay suficiente stock"""
        return self.stock >= cantidad