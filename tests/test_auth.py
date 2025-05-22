from tests.conftest import client


def test_unauthorized_access_to_create_order(new_product):
    r = client.post("/orders/", json={"product_id": new_product.id})
    assert r.status_code == 403

def test_forbidden_status_change_by_accountant(old_product, client_auth_accountant, client_auth_cashier):
    order = client.post("/orders/",
        headers=client_auth_cashier,
        json={"product_id": old_product.id}
    ).json()

    r = client.patch(f"/orders/{order['id']}/status",
        headers=client_auth_accountant,
        json={"status": "done"}
    )
    assert r.status_code == 403
