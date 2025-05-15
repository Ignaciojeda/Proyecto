from flask import Blueprint, request, jsonify, current_app,render_template
import requests
from transbank.webpay.webpay_plus.transaction import Transaction

webpay_bp = Blueprint('webpay', __name__)

def get_webpay_headers():
    """Obtiene los headers para las solicitudes a Webpay"""
    return {
        "Tbk-Api-Key-Id": current_app.config['COMMERCE_CODE'],
        "Tbk-Api-Key-Secret": current_app.config['API_KEY'],
        "Content-Type": "application/json"
    }

@webpay_bp.route('/webpay/crear', methods=['POST'])
def crear_transaccion():
    try:
        data = request.json
        required_fields = ['buy_order', 'session_id', 'amount']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        payload = {
            "buy_order": data['buy_order'],
            "session_id": data['session_id'],
            "amount": data['amount'],
            "return_url": current_app.config['RETURN_URL']
        }
        
        response = requests.post(
            f"{current_app.config['WEBPAY_URL']}/transactions",
            json=payload,
            headers=get_webpay_headers()
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@webpay_bp.route('/webpay/confirmar/<token>', methods=['GET'])
def confirmar_transaccion(token):
    try:
        response = requests.get(
            f"{current_app.config['WEBPAY_URL']}/transactions/{token}",
            headers=get_webpay_headers()
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    





@webpay_bp.route('/confirmacion', methods=['GET', 'POST'])
def confirmacion_pago():
    token_ws = request.args.get('token_ws')
    
    if not token_ws:
        return render_template('error.html', mensaje="No se recibió el token de pago.")

    response = Transaction().commit(token_ws)
    
    if response['status'] == 'AUTHORIZED':
        estado_pago = "Pago procesado exitosamente."
    else:
        estado_pago = f"Pago no procesado. Estado: {response['status']}"
    
    return render_template('Pago_Realizado.html', estado_pago=estado_pago)

