from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate 


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app) 


    # Inicializar Migrate y ejecutar migraciones
    migrate = Migrate(app, db)
    with app.app_context():
        try:
            migrate.init_app(app)
        except Exception as e:
            print(f"Error al inicializar las migraciones: {e}")

    # Registrar blueprints
    from .Controlador.Objeto_Controlador import objeto_bp
    app.register_blueprint(objeto_bp)

    from .Controlador.Listar_Objeto import listar_bp
    app.register_blueprint(listar_bp)

    return app