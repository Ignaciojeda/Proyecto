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
    from app.Modelo.Producto import Producto
    from app.Modelo.Categoria import Categoria
    from app.Modelo.Inventario import Inventario

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página." 
    login_manager.login_message_category = "info"  

    # Definir el filtro de base64
    def b64encode(value):
        return base64.b64encode(value).decode('utf-8')

    # Registrar el filtro en Jinja2
    app.jinja_env.filters['b64encode'] = b64encode

    from app.Controlador.Login import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.Controlador.Rutas import login_bp
    app.register_blueprint(login_bp)

    from app.Controlador.Catalogo import catalogo_bp
    app.register_blueprint(catalogo_bp, url_prefix='/catalogo')
    
    from app.Controlador.Carrito import carrito_bp
    app.register_blueprint(carrito_bp, url_prefix='/carrito')
    
    from app.Controlador.Pedidos import pedidos_bp
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    
    from app.Controlador.Perfil import perfil_bp
    app.register_blueprint(perfil_bp, url_prefix='/perfil')
    
    from app.Controlador.Crear_Usuario import usuario_bp
    app.register_blueprint(usuario_bp)

    from app.Controlador.Home import home_bp
    app.register_blueprint(home_bp, url_prefix='/home')

    from app.Controlador.Home_Admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.Controlador.Registro_Admin import admin_registro_bp
    app.register_blueprint(admin_registro_bp, url_prefix='/admin/registro')
    
    from app.Controlador.Registro_Producto import producto_bp
    app.register_blueprint(producto_bp, url_prefix='/admin/productos')

    from app.Controlador.Vista_Bodeguero import bodeguero_bp
    app.register_blueprint(bodeguero_bp, url_prefix='/bodeguero')
    
    from app.Controlador.Vista_Contador import contador_bp
    app.register_blueprint(contador_bp, url_prefix='/contador')
    

    try:
        from app.Controlador.Webpay import webpay_bp
        app.register_blueprint(webpay_bp, url_prefix='/api')
    except ImportError:
        pass

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.Modelo.Usuario import Usuario
    return Usuario.query.get(int(user_id))