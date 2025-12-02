from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_full_order_flow():
    order_payload = {
        "customer_name": "Integration Tester",
        "description": "Checking flow",
        "total_price": 25.50,
        "order_status": "Pending"
    }
    response_order = client.post("/orders/", json=order_payload)
    assert response_order.status_code == 200
    order_id = response_order.json()["id"]
    assert response_order.json()["order_status"] == "Pending"

    payment_payload = {
        "order_id": order_id,
        "amount": 25.50,
        "payment_type": "Credit Card",
        "transaction_status": "Success",
        "transaction_id": "ch_12345",
        "last_4_digits": "4242",
        "card_brand": "Visa"
    }
    response_payment = client.post("/payments/", json=payment_payload)
    assert response_payment.status_code == 200

    response_check = client.get(f"/orders/{order_id}")
    assert response_check.status_code == 200
    assert response_check.json()["order_status"] == "Processing"
