from flask import Blueprint, render_template, request, current_app, jsonify
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType

webpay_bp = Blueprint('webpay', __name__)

@webpay_bp.route('/webpay/formulario/', methods=['GET', 'POST'])
def webpay_formulario():
    if request.method == 'POST':
        buy_order = request.form.get('buy_order')
        session_id = request.form.get('session_id')
        amount = request.form.get('amount')
        return_url = request.host_url + 'webpay/retorno/'

        config = current_app.config['TRANSBANK']
        options = WebpayOptions(
            commerce_code=config['commerce_code'],
            api_key=config['api_key'],
            integration_type=IntegrationType.TEST
        )
        transaction = Transaction(options)
        response = transaction.create(buy_order, session_id, amount, return_url)

        return render_template('verificar.html', url=response['url'], token=response['token'])

    return render_template('form.html')

@webpay_bp.route('/webpay/retorno/', methods=['POST'])
def webpay_retorno():
    token_ws = request.form.get('token_ws')
    if not token_ws:
        return jsonify({'error': 'token_ws es requerido'}), 400

    config = current_app.config['TRANSBANK']
    options = WebpayOptions(
        commerce_code=config['commerce_code'],
        api_key=config['api_key'],
        integration_type=IntegrationType.TEST
    )
    transaction = Transaction(options)
    result = transaction.status(token_ws)
    return jsonify(result)
