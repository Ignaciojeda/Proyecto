from app import db
from datetime import date

class Comentario(db.Model):
    __tablename__ = 'COMENTARIO'

    idComentario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productoId = db.Column(db.Integer, db.ForeignKey('PRODUCTO.idProducto'), nullable=False)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'), nullable=False)
    
    comentario = db.Column(db.Text, nullable=False)  
    calificacion = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)


    producto = db.relationship('Producto', back_populates='comentarios')
    usuario = db.relationship('Usuario', back_populates='comentarios')

    def __repr__(self):
        return f'<Comentario {self.idComentario} por Usuario {self.usuarioId} sobre Producto {self.productoId}>'
