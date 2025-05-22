from enum import Enum

class Currency(str, Enum):
    UAH = "UAH"
    USD = "USD"
    EUR = "EUR"

class OrderStatus(str, Enum):
    CREATED = "created"
    DONE = "done"
    PAID = "paid"
