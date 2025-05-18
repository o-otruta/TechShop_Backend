from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_create_order_with_discount(old_product, client_auth_cashier):
    response = client.post("/orders/", headers=client_auth_cashier, json={
        "product_id": old_product["id"]
    })
    assert response.status_code == 200
    order = response.json()
    assert order["discount_applied"] is True
    assert order["final_price"] < old_product["price"]

def test_create_order(client_auth_cashier, old_product):
    response = client.post("/orders/", headers=client_auth_cashier, json={
        "product_id": old_product["id"]
    })
    assert response.status_code == 200
    order = response.json()
    assert "id" in order
    assert order["product"]["id"] == old_product["id"]

def test_create_invoice(client_auth_cashier, old_product):
    order_response = client.post("/orders/", headers=client_auth_cashier, json={
        "product_id": old_product["id"]
    })
    order = order_response.json()

    invoice_response = client.post(f"/invoices/create/{order['id']}", headers=client_auth_cashier)
    assert invoice_response.status_code == 200
    invoice = invoice_response.json()
    assert invoice["order"]["id"] == order["id"]

def test_update_order_status(client_auth_cashier, client_auth_consultant, old_product):
    order_response = client.post("/orders/", headers=client_auth_cashier, json={
        "product_id": old_product["id"]
    })
    order = order_response.json()

    status_response = client.patch(f"/orders/{order['id']}/status", headers=client_auth_consultant, json={
        "status": "done"
    })
    assert status_response.status_code == 200
    updated_order = status_response.json()
    assert updated_order["status"] == "done"

def test_accountant_can_see_orders_in_date_range(client_auth_cashier, client_auth_accountant, old_product):
    order_response = client.post("/orders/", headers=client_auth_cashier, json={
        "product_id": old_product["id"]
    })
    assert order_response.status_code == 200
    order = order_response.json()

    created_date = datetime.fromisoformat(order["created_at"])
    from_date = created_date.strftime("%Y-%m-%d")
    to_date = (created_date + timedelta(days=1)).strftime("%Y-%m-%d")

    report_response = client.get(f"/orders/report?from={from_date}&to={to_date}", headers=client_auth_accountant)
    assert report_response.status_code == 200
    report = report_response.json()

    matching = [o for o in report if o["id"] == order["id"]]
    assert len(matching) == 1
