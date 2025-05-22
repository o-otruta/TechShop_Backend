from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_create_order_with_discount(old_product, client_auth_cashier):
    response = client.post("/orders/",
        headers=client_auth_cashier,
        json={"product_id": old_product.id}
    )
    assert response.status_code == 200
    order = response.json()
    assert order["discount_applied"] is True
    assert order["final_price"] < old_product.price

def test_create_order_and_invoice(new_product, client_auth_cashier):
    response = client.post("/orders/",
        headers=client_auth_cashier,
        json={"product_id": new_product.id}
    )
    assert response.status_code == 200
    order = response.json()
    assert order["product"]["id"] == new_product.id

    inv_resp = client.post(f"/invoices/create/{order['id']}",
        headers=client_auth_cashier
    )
    assert inv_resp.status_code == 200
    invoice = inv_resp.json()
    assert invoice["order"]["id"] == order["id"]

def test_update_order_status(old_product, client_auth_cashier, client_auth_consultant):
    order_resp = client.post("/orders/",
        headers=client_auth_cashier,
        json={"product_id": old_product.id}
    )
    order = order_resp.json()

    status_resp = client.patch(f"/orders/{order['id']}/status",
        headers=client_auth_consultant,
        json={"status": "done"}
    )
    assert status_resp.status_code == 200
    updated = status_resp.json()
    assert updated["status"] == "done"

