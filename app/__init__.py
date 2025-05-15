import os
import base64
from datetime import datetime
from flask import current_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Configurar filtros de plantilla
    configure_template_filters(app)

    # Registrar blueprints
    register_blueprints(app)

    # Configurar loader de usuario
    configure_user_loader()

    return app

def configure_template_filters(app):
    # Formato de moneda
    @app.template_filter('currency')
    def currency_filter(value, currency):
        try:
            value = float(value)
            if currency == 'CLP':
                return f"${value:,.0f}".replace(",", ".") + " CLP"
            elif currency == 'USD':
                return f"US${value:,.2f}"
            elif currency == 'EUR':
                return f"€{value:,.2f}"
            elif currency == 'BRL':
                return f"R${value:,.2f}"
            elif currency == 'COP':
                return f"${value:,.0f} COP"
            elif currency == 'MXN':
                return f"${value:,.2f} MXN"
            return f"{value:,.2f} {currency}"
        except:
            return str(value)

    # Formato de fecha
    @app.template_filter('datetimeformat')
    def datetimeformat_filter(value, format):
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value.strftime(format)

    # Filtro para base64
    @app.template_filter('b64encode')
    def b64encode_filter(value):
        return base64.b64encode(value).decode('utf-8')

def register_blueprints(app):
    from app.Controlador.Login import auth_bp
    from app.Controlador.Rutas import login_bp
    from app.Controlador.Catalogo import catalogo_bp
    from app.Controlador.Carrito import carrito_bp
    from app.Controlador.Pedidos import pedidos_bp
    from app.Controlador.Perfil import perfil_bp
    from app.Controlador.Crear_Usuario import usuario_bp
    from app.Controlador.Home import home_bp
    from app.Controlador.Home_Admin import admin_bp
    from app.Controlador.Registro_Admin import admin_registro_bp
    from app.Controlador.Registro_Producto import producto_bp
    from app.Controlador.Vista_Bodeguero import bodeguero_bp
    from app.Controlador.Vista_Contador import contador_bp
    from app.Controlador.API.Divisas_Api import api_divisas_bp

    # APIs (si están disponibles)
    try:
        from app.Controlador.API import producto_api_bp, divisas_api_bp, auth_api_bp
        app.register_blueprint(producto_api_bp)
        app.register_blueprint(divisas_api_bp)
        app.register_blueprint(auth_api_bp)
    except ImportError:
        pass

    app.register_blueprint(auth_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(api_divisas_bp)
    app.register_blueprint(catalogo_bp, url_prefix='/catalogo')
    app.register_blueprint(carrito_bp, url_prefix='/carrito')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(perfil_bp, url_prefix='/perfil')
    app.register_blueprint(usuario_bp)
    app.register_blueprint(home_bp, url_prefix='/home')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(admin_registro_bp, url_prefix='/admin/registro')
    app.register_blueprint(producto_bp, url_prefix='/admin/productos')
    app.register_blueprint(bodeguero_bp, url_prefix='/bodeguero')
    app.register_blueprint(contador_bp, url_prefix='/contador')
    

    # Registrar Webpay si está disponible
    try:
        from app.Controlador.Webpay import webpay_bp
        app.register_blueprint(webpay_bp, url_prefix='/webpay')
    except ImportError:
        pass

def configure_user_loader():
    @login_manager.user_loader
    def load_user(user_id):
        from app.Modelo.Usuario import Usuario
        return Usuario.query.get(int(user_id))
