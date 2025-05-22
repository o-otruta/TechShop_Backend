from datetime import datetime, timedelta
from tests.conftest import client

def test_empty_report_for_no_orders(client_auth_accountant):
    r = client.get("/orders/report?from=2100-01-01&to=2100-01-02",
                   headers=client_auth_accountant)
    assert r.status_code == 200
    assert r.json() == []

def test_report_includes_order(old_product, client_auth_cashier, client_auth_accountant):
    order = client.post("/orders/",
                        headers=client_auth_cashier,
                        json={"product_id": old_product.id}
                       ).json()
    created = datetime.fromisoformat(order["created_at"])
    frm = created.strftime("%Y-%m-%d")
    to  = (created + timedelta(days=1)).strftime("%Y-%m-%d")

    report = client.get(f"/orders/report?from={frm}&to={to}",
                        headers=client_auth_accountant
                       ).json()
    assert any(o["id"] == order["id"] for o in report)
