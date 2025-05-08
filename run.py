from flask import Flask

from app.Controlador.Rutas import home_bp
from app.Controlador.Login import auth_bp
from app.Controlador.Crear_Usuario import usuario_bp
from app.Controlador.Webpay import webpay_bp


app = Flask(__name__)

# Registrar el Blueprint del objeto

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(webpay_bp)

if __name__ == '__main__':
    app.run(debug=True)
