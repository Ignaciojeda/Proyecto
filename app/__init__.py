from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate 
from flask_login import LoginManager
import base64

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.Modelo.Usuario import Usuario
    from app.Modelo.Pedido import Pedido
    from app.Modelo.Sucursal import Sucursal
    from app.Modelo.EtapaPedido import EtapaPedido
    from app.Modelo.Marca import Marca
    from app.Modelo.TipoUsuario import TipoUsuario
    

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página." 
    login_manager.login_message_category = "info"  

    # Definir el filtro de base64
    def b64encode(value):
        return base64.b64encode(value).decode('utf-8')

    # Registrar el filtro en Jinja2
    app.jinja_env.filters['b64encode'] = b64encode

    # Registrar blueprints
  
    
    from .Controlador.Rutas import login_bp  
    app.register_blueprint(login_bp) 

    from .Controlador.Login import auth_bp  
    app.register_blueprint(auth_bp)  


    from .Controlador.Crear_Usuario import usuario_bp
    app.register_blueprint(usuario_bp)

    from .Controlador.Catalogo import catalogo_bp
    app.register_blueprint(catalogo_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.Modelo.Usuario import Usuario  
    return Usuario.query.get(int(user_id))
