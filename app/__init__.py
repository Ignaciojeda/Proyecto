from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Mover la inicialización de Migrate dentro de la función create_app
    migrate = Migrate(app, db)

    # Registro del blueprint de los controladores
    from .Controlador.Objeto_Controlador import objeto_bp
    app.register_blueprint(objeto_bp)

    return app
