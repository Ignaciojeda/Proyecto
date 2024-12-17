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

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página." 
    login_manager.login_message_category = "info"  

    def b64encode(value):
        return base64.b64encode(value).decode('utf-8')

    app.jinja_env.filters['b64encode'] = b64encode

    from .Controlador.Objeto_Controlador import objeto_bp
    app.register_blueprint(objeto_bp)

    from .Controlador.Listar_Objeto import listar_bp
    app.register_blueprint(listar_bp)
    
    from .Controlador.Rutas import login_bp  
    app.register_blueprint(login_bp) 

    from .Controlador.Login import auth_bp  
    app.register_blueprint(auth_bp)  

    from .Controlador.Historial import historial_bp
    app.register_blueprint(historial_bp) 

    from .Controlador.Crear_Usuario import usuario_bp
    app.register_blueprint(usuario_bp)

    from app.Controlador.Listar_Objeto_Admin import listara_bp  
    app.register_blueprint(listara_bp) 

    from app.Controlador.Entregar_Objeto import entregar_bp 
    app.register_blueprint(entregar_bp, url_prefix='/entregar')

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.Modelo.Usuario import Usuario  
    return Usuario.query.get(str(user_id))

