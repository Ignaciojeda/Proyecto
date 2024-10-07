from flask import Flask
from app.Controlador.Objeto_Controlador import objeto_bp

app = Flask(__name__)

# Registrar el Blueprint del objeto perdido
app.register_blueprint(objeto_bp)

if __name__ == '__main__':
    app.run(debug=True)
