from flask import Flask
from app.Controlador.Objeto_Controlador import objeto_bp
from app.Controlador.Listar_Objeto import listar_bp    

app = Flask(__name__)

# Registrar el Blueprint del objeto
app.register_blueprint(objeto_bp)
app.register_blueprint(listar_bp)

if __name__ == '__main__':
    app.run(debug=True)
