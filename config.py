# config.py
import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://ucuut7lyq0o6mltn:ZYquvLhikMUiw1liSVKY'
        '@bp0xjhrmff7pogi61dt0-mysql.services.clever-cloud.com:3306/bp0xjhrmff7pogi61dt0'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    COMMERCE_CODE = '597055555532'
    API_KEY = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
    WEBPAY_URL = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.3'
    RETURN_URL = 'http://127.0.0.1:5000/webpay/commit'


    BANCO_CENTRAL_API_URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    BANCO_CENTRAL_USER = "ignacioojeda0066@gmail.com" 
    BANCO_CENTRAL_PASS = "Ignacio03"
    

    SERIES_DIVISAS = {
        'USD': 'F073.TCO.PRE.USD.CLP',
        'EUR': 'F073.TCO.PRE.EUR.CLP',
        'BRL': 'F073.TCO.PRE.BRL.CLP',
        'COP': 'F073.TCO.PRE.COP.CLP',
        'MXN': 'F073.TCO.PRE.MXN.CLP'
    }
    
    MONEDA_LOCAL = 'CLP'
    MONEDAS_SOPORTADAS = list(SERIES_DIVISAS.keys())
    
