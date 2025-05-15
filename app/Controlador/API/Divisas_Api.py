from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required
from app.Services.Conversor_Divisas import ServicioDivisas
from app import current_app

api_divisas_bp = Blueprint('api_divisas', __name__, url_prefix='/api/v1')

@api_divisas_bp.route('/divisas/convertir', methods=['GET'])
def convertir_divisa():
    try:
        # Validar parámetros
        monto = float(request.args.get('monto', 1.0))
        moneda_origen = request.args.get('origen', 'USD').upper()
        moneda_destino = request.args.get('destino', current_app.config['MONEDA_LOCAL']).upper()
        
        # Validar monedas soportadas
        if (moneda_origen not in current_app.config['MONEDAS_SOPORTADAS'] and 
            moneda_origen != current_app.config['MONEDA_LOCAL']):
            return jsonify({
                'error': f'Moneda origen {moneda_origen} no soportada',
                'monedas_soportadas': current_app.config['MONEDAS_SOPORTADAS']
            }), 400
            
        if (moneda_destino not in current_app.config['MONEDAS_SOPORTADAS'] and 
            moneda_destino != current_app.config['MONEDA_LOCAL']):
            return jsonify({
                'error': f'Moneda destino {moneda_destino} no soportada',
                'monedas_soportadas': current_app.config['MONEDAS_SOPORTADAS']
            }), 400
        
        # Realizar conversión
        resultado = ServicioDivisas.convertir(monto, moneda_origen, moneda_destino)
        
        return jsonify({
            'monto_original': monto,
            'moneda_origen': moneda_origen,
            'moneda_destino': moneda_destino,
            'monto_convertido': round(resultado, 2),
            'fecha_actualizacion': datetime.now().isoformat()
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Monto debe ser numérico'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_divisas_bp.route('/divisas/tasas', methods=['GET'])
def obtener_tasas():
    try:
        tasas = {}
        for moneda in current_app.config['MONEDAS_SOPORTADAS']:
            tasas[moneda] = {
                'tasa': ServicioDivisas.obtener_tasa_actual(moneda),
                'fecha': datetime.now().isoformat()
            }
        
        return jsonify(tasas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_divisas_bp.route('/divisas/series', methods=['GET'])
@jwt_required()
def obtener_series():
    """Endpoint administrativo para explorar series disponibles"""
    try:
        series = ServicioDivisas.obtener_series_disponibles()
        return jsonify(series), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500