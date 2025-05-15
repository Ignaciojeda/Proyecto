from flask import Blueprint, request, jsonify, current_app, redirect, render_template

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

@webpay_bp.route('/webpay/crear', methods=['GET', 'POST'])
def crear_transaccion():
    if request.method == 'GET':
        return render_template('webpay_form.html')

    try:
        data = request.form
        required_fields = ['buy_order', 'session_id', 'amount']

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos requeridos'}), 400

        payload = {
            "buy_order": data['buy_order'],
            "session_id": data['session_id'],
            "amount": int(data['amount']),
            "return_url": current_app.config['RETURN_URL']
            # Eliminado el cancel_url que no es soportado
        }

        response = requests.post(
            f"{current_app.config['WEBPAY_URL']}/transactions",
            json=payload,
            headers=get_webpay_headers()
        )

        if response.status_code == 200:
            resp_json = response.json()
            return redirect(resp_json['url'] + '?token_ws=' + resp_json['token'])

        return jsonify(response.json()), response.status_code

    except Exception as e:
        current_app.logger.error(f"Error en crear_transaccion: {str(e)}")
        return jsonify({'error': str(e)}), 500

@webpay_bp.route('/webpay/confirmar/<token>', methods=['GET'])
def confirmar_transaccion(token):
    try:
        response = requests.get(
            f"{current_app.config['WEBPAY_URL']}/transactions/{token}",
            headers=get_webpay_headers()
        )
        data = response.json()

        if response.status_code == 200:
            return render_template("webpay_exito.html", data=data)
        else:
            return render_template("webpay_error.html", data=data)

    except Exception as e:
        return f"Error confirmando transacción: {str(e)}", 500
    

@webpay_bp.route('/webpay/commit', methods=['GET', 'POST'])
def webpay_commit():
    token = request.args.get('token_ws')
    if not token:
        return "Token no recibido", 400
    return redirect(f"/webpay/confirmar/{token}")
