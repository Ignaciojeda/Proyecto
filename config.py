import os

class Config:
    SECRET_KEY = os.urandom(24)  # Llave secreta para sesiones y seguridad

    # Configuración de conexión a la base de datos en Clever Cloud
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://umioqejykf1rosez:'
        'AwX7vAF5qCJbQBurc4Mp'
        '@bberwxnczvkakxyarepa-mysql.services.clever-cloud.com:3306/'
        'bberwxnczvkakxyarepa'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
