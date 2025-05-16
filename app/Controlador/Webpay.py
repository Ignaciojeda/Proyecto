from flask import Blueprint, request, jsonify, current_app, redirect, render_template, session
from flask_login import current_user
from app.Modelo.Carrito import Carrito
from app.Modelo.Pedido import Pedido
from app.Modelo.DetallePedido import DetallePedido  # Asegúrate de importar tu modelo
from app import db
from decimal import Decimal
from datetime import datetime



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

@webpay_bp.route('/crear', methods=['GET', 'POST'])
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
        }

        response = requests.post(
            f"{current_app.config['WEBPAY_URL']}/transactions",
            json=payload,
            headers=get_webpay_headers()
        )

        if response.status_code == 200:
            # Guardar el ID del usuario en la sesión antes de redirigir
            

            resp_json = response.json()
            return redirect(resp_json['url'] + '?token_ws=' + resp_json['token'])

        return jsonify(response.json()), response.status_code

    except Exception as e:
        current_app.logger.error(f"Error en crear_transaccion: {str(e)}")
        return jsonify({'error': str(e)}), 500

@webpay_bp.route('/confirmar/<token>', methods=['GET'])
def confirmar_transaccion(token):
    try:
        response = requests.get(
            f"{current_app.config['WEBPAY_URL']}/transactions/{token}",
            headers=get_webpay_headers()
        )
        data = response.json()
        print("Webpay respuesta:", data)

        if response.status_code == 200 and data.get('status') == 'AUTHORIZED':
            # Asegúrate de que el usuario esté autenticado
            if not current_user.is_authenticated:
                return "Usuario no autenticado", 403

            usuario_id = current_user.idUsuario

            # Paso 1: Obtener los ítems del carrito
            carrito_items = Carrito.query.filter_by(usuarioId=usuario_id).all()
            if not carrito_items:
                return "No hay productos en el carrito", 400

            # Paso 2: Calcular el total del pedido
            total = sum(item.precio * item.cantidad for item in carrito_items)

            # Paso 3: Crear el Pedido
            nuevo_pedido = Pedido(
                clienteId=usuario_id,
                total=Decimal(total),
                direccionEnvio="Dirección de ejemplo",
                sucursalID=None,
                etapaId=1
            )
            db.session.add(nuevo_pedido)
            db.session.commit()  # Necesario para obtener el ID del pedido

            # Paso 4: Añadir los detalles del pedido
            for item in carrito_items:
                detalle = DetallePedido(
                    pedidoId=nuevo_pedido.idPedido,
                    productoId=item.productoId,
                    cantidad=item.cantidad,
                    precio=item.precio
                )
                db.session.add(detalle)

            db.session.commit()  # Guardar todos los detalles

            # Paso 5: Limpiar el carrito del usuario
            for item in carrito_items:
                db.session.delete(item)
            db.session.commit()

            session.pop('usuario_id', None)

            return render_template("webpay_exito.html", data=data)

        else:
            return render_template("webpay_error.html", data=data)

    except Exception as e:
        return f"Error confirmando transacción: {str(e)}", 500


@webpay_bp.route('/commit', methods=['GET', 'POST'])
def webpay_commit():
    token = request.args.get('token_ws')
    if not token:
        return "Token no recibido", 400

    try:
        response = requests.put(
            f"{current_app.config['WEBPAY_URL']}/transactions/{token}",
            headers=get_webpay_headers()
        )
        data = response.json()

        if response.status_code == 200 and data.get("status") == "AUTHORIZED":
            return redirect(f"/webpay/confirmar/{token}")
        else:
            return render_template("webpay_error.html", data=data)

    except Exception as e:
        return f"Error en commit de transacción: {str(e)}", 500
