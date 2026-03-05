import requests
import uuid
from django.conf import settings

def initiate_ecocash_payment(msisdn, amount, order_id):
    url = settings.ECOCASH_C2B_SANDBOX_URL

    payload = {
        "customerMsisdn": msisdn,
        "amount": float(amount),
        "reason": f"Order #{order_id}",
        "currency": "USD",
        "sourceReference": str(uuid.uuid4())
    }

    headers = {
        "X-API-KEY": settings.ECOCASH_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response
