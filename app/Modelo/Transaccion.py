# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True)
    orden = db.Column(db.String(50))
    sesion = db.Column(db.String(50))
    monto = db.Column(db.Float)
    estado = db.Column(db.String(50))
