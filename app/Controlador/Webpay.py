import requests
import config

HEADERS = {
    "Tbk-Api-Id:": config.COMMERCE_CODE,
    "Tbk-Api-Key:": config.API_KEY,
    "Content-Type": "application/json"
}

def create_transaction(buy_order, session_id, amount):
    payload = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": config.RETURN_URL
    }
    response = requests.post(f"{config.WEBPAY_URL}/transactions", json=payload, headers=HEADERS)
    return response.json()

def commit_transaction(token):
    print(token)
    response = requests.get(f"{config.WEBPAY_URL}/transactions/{token}", headers=HEADERS)
    return response.json()

