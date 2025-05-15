import requests
from datetime import datetime, timedelta
from flask import current_app
from cachetools import TTLCache
import xml.etree.ElementTree as ET

# Cache para almacenar tasas (válidas por 1 hora)
cache = TTLCache(maxsize=100, ttl=3600)

class ServicioDivisas:
    @staticmethod
    def obtener_tasa_actual(moneda_extranjera):
        """Obtiene la tasa de cambio actual desde el Banco Central"""
        if moneda_extranjera == current_app.config['MONEDA_LOCAL']:
            return 1.0
        
        try:
            # Verificar cache primero
            cache_key = f"tasa_{moneda_extranjera}"
            if cache_key in cache:
                return cache[cache_key]
                
            # Obtener serie del config
            serie = current_app.config['SERIES_DIVISAS'].get(moneda_extranjera)
            if not serie:
                raise ValueError(f"Moneda {moneda_extranjera} no soportada")
            
            # Parámetros para la API
            params = {
                'user': current_app.config['BANCO_CENTRAL_USER'],
                'pass': current_app.config['BANCO_CENTRAL_PASS'],
                'firstdate': datetime.now().strftime('%Y-%m-%d'),
                'timeseries': serie,
                'function': 'GetSeries'
            }
            
            # Llamada a la API
            response = requests.get(
                current_app.config['BANCO_CENTRAL_API_URL'],
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                # Parsear respuesta XML (la API devuelve XML aunque pidas JSON)
                root = ET.fromstring(response.content)
                series = root.find('Series')
                
                if series is not None:
                    obs = series.find('Obs')
                    if obs is not None:
                        tasa = float(obs.find('value').text)
                        cache[cache_key] = tasa
                        return tasa
            
            # Fallback a tasas de respaldo si la API falla
            return ServicioDivisas.tasa_respaldo(moneda_extranjera)
            
        except Exception as e:
            current_app.logger.error(f"Error obteniendo tasa {moneda_extranjera}: {str(e)}")
            return ServicioDivisas.tasa_respaldo(moneda_extranjera)
    
    @staticmethod
    def tasa_respaldo(moneda_extranjera):
        """Tasas de respaldo actualizadas manualmente"""
        tasas = {
            'USD': 950.0,
            'EUR': 1020.0,
            'BRL': 180.0,
            'COP': 0.22,
            'MXN': 50.0
        }
        return tasas.get(moneda_extranjera, 1.0)
    
    @staticmethod
    def convertir(monto, moneda_origen, moneda_destino):
        """Convierte un monto entre monedas"""
        if moneda_origen == moneda_destino:
            return monto
            
        # Convertir primero a CLP si es necesario
        if moneda_origen != current_app.config['MONEDA_LOCAL']:
            tasa_origen = ServicioDivisas.obtener_tasa_actual(moneda_origen)
            monto_clp = monto / tasa_origen
        else:
            monto_clp = monto
            
        # Convertir a moneda destino si es necesario
        if moneda_destino != current_app.config['MONEDA_LOCAL']:
            tasa_destino = ServicioDivisas.obtener_tasa_actual(moneda_destino)
            return monto_clp * tasa_destino
            
        return monto_clp
    
    @staticmethod
    def obtener_series_disponibles():
        """Obtiene el listado de series disponibles del Banco Central"""
        try:
            params = {
                'user': current_app.config['BANCO_CENTRAL_USER'],
                'pass': current_app.config['BANCO_CENTRAL_PASS'],
                'function': 'SearchSeries',
                'frequency': 'DAILY'
            }
            
            response = requests.get(
                current_app.config['BANCO_CENTRAL_API_URL'],
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                series_infos = []
                
                for info in root.findall('SeriesInfos/Info'):
                    series_infos.append({
                        'id': info.find('seriesId').text,
                        'titulo_es': info.find('spanishTitle').text,
                        'titulo_en': info.find('englishTitle').text,
                        'frecuencia': info.find('frequencyCode').text,
                        'primera_obs': info.find('firstObservation').text,
                        'ultima_obs': info.find('lastObservation').text
                    })
                
                return series_infos
                
        except Exception as e:
            current_app.logger.error(f"Error obteniendo series: {str(e)}")
        
        return []