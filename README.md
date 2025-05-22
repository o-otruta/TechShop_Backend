# TechShopBackend

This project implements a backend system for managing orders in a tech store using FastAPI and SQLite.

- RESTful API
- Three user roles:
  - `cashier`: creates orders, generates invoices, payments
  - `consultant`: update orders status
  - `accountant`: accesses orders reports
- 20% discount on products older than 30 days
- Swagger documentation (`localhost:8000/docs`)
- Unit tests with pytest
- Postman collection included

## Installation
NOTE: Requires Python 3.12+.
```bash
git clone https://github.com/o-otruta/TechShop_Backend.git
python -m venv .venv
source .venv/bin/activate  # for windows: .venv/Scripts/activate
pip install -r requirements.txt
```

## Run app

```bash
uvicorn app.main:app
```
Go to: http://localhost:8000/docs

## Run tests

```bash
pytest
```

## Assets

- `fixtures.py` : run to create five products
- `TechShopBackend.postman_collection.json` : postman collection


