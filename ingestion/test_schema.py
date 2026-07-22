from schema import RetailTransaction


sample_transaction = {
    "invoice_no": "536365",
    "stock_code": "85123A",
    "description": "WHITE HANGING HEART T-LIGHT HOLDER",
    "quantity": 6,
    "invoice_date": "2010-12-01 08:26:00",
    "unit_price": 2.55,
    "customer_id": 17850,
    "country": "United Kingdom",
}


transaction = RetailTransaction(**sample_transaction)

print(transaction)
print("Transaction is valid.")