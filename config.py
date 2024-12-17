import os

class Config:
    SECRET_KEY = os.urandom(24)  
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://umioqejykf1rosez:'
        'AwX7vAF5qCJbQBurc4Mp'
        '@bberwxnczvkakxyarepa-mysql.services.clever-cloud.com:3306/'
        'bberwxnczvkakxyarepa'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
