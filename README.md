# TechShopBackend

This project implements a backend system for managing orders in a tech store using FastAPI and SQLite.

## About

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

```bash
git clone https://github.com/your-username/techshop-backend.git
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

- **fixtures.py** : creates five products


