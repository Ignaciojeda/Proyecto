from flask import Flask
from app.Controlador.Objeto_Controlador import objeto_bp
from app.Controlador.Listar_Objeto import listar_bp    
from app.Controlador.Historial import historial_bp
from app.Controlador.Rutas import home_bp
from app.Controlador.Login import auth_bp
from app.Controlador.Crear_Usuario import usuario_bp

app = Flask(__name__)

# Registrar el Blueprint del objeto
app.register_blueprint(objeto_bp)
app.register_blueprint(listar_bp)
app.register_blueprint(historial_bp)
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(usuario_bp)

if __name__ == '__main__':
    app.run(debug=True)
