from pydantic import ValidationError

from schema import RetailTransaction


valid_transaction = {
    "invoice_no": "536365",
    "stock_code": "85123A",
    "description": "WHITE HANGING HEART T-LIGHT HOLDER",
    "quantity": 6,
    "invoice_date": "2010-12-01 08:26:00",
    "unit_price": 2.55,
    "customer_id": 17850,
    "country": "United Kingdom",
}


invalid_transaction = {
    "invoice_no": "536365",
    "stock_code": "85123A",
    "description": "WHITE HANGING HEART T-LIGHT HOLDER",
    "quantity": "invalid quantity",
    "invoice_date": "2010-12-01 08:26:00",
    "unit_price": 2.55,
    "customer_id": 17850,
    "country": "United Kingdom",
}


valid_result = RetailTransaction(**valid_transaction)
print("Valid transaction accepted.")


try:
    RetailTransaction(**invalid_transaction)

except ValidationError:
    print("Invalid transaction rejected.")