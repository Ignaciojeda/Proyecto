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

    TRANSBANK = {
        'commerce_code': '597055555532',
        'api_key': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'environment': 'TEST'
        'return_url': 'http://localhost:5000/webpay/commit'
    }
