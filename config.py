import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://ucuut7lyq0o6mltn:'
        'ZYquvLhikMUiw1liSVKY'
        '@bp0xjhrmff7pogi61dt0-mysql.services.clever-cloud.com:3306/'
        'bp0xjhrmff7pogi61dt0'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

