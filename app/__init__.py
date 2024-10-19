from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate 
import base64

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Registrar blueprints
    from .Controlador.Objeto_Controlador import objeto_bp
    app.register_blueprint(objeto_bp)

    from .Controlador.Listar_Objeto import listar_bp
    app.register_blueprint(listar_bp)

    # Registrar el blueprint de Home
    from .Controlador.Objeto_Controlador import home_bp  # Importa el blueprint que acabas de crear
    app.register_blueprint(home_bp)  # Registra el blueprint

    # Filtro de base64 para imágenes
    @app.template_filter('b64encode')
    def b64encode_filter(data):
        if data:
            return base64.b64encode(data).decode('utf-8')
        return ''

    return app
