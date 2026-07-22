from datetime import datetime

from pydantic import BaseModel, Field


class RetailTransaction(BaseModel):
    invoice_no: str
    stock_code: str
    description: str | None
    quantity: int
    invoice_date: datetime
    unit_price: float = Field(ge=0)
    customer_id: float | None
    country: str