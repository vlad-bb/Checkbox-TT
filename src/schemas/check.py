from pydantic import BaseModel, condecimal, conint
from datetime import datetime
from typing import List, Literal


class ProductRequest(BaseModel):
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    quantity: conint(gt=0)


class PaymentRequest(BaseModel):
    type: Literal["cash", "cashless"]
    amount: condecimal(max_digits=10, decimal_places=2)


class CheckRequest(BaseModel):
    products: List[ProductRequest]
    payment: PaymentRequest

    class Config:
        json_schema_extra = {
            "example": {
                "products": [
                    {
                        "name": "Mavic 3T",
                        "price": 298_870.50,
                        "quantity": 3,
                    }
                ],
                "payment": {
                    "type": "cash",
                    "amount": 896_611.50
,
                },
            }

        }


class ProductResponse(ProductRequest):
    total: condecimal(max_digits=10, decimal_places=2)


class PaymentResponse(PaymentRequest):
    pass


class CheckResponse(BaseModel):
    id: int
    products: List[ProductResponse]
    payment: PaymentResponse
    total: condecimal(max_digits=10, decimal_places=2)
    rest: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime

class CheckResponseList(BaseModel):
    entries: List[CheckResponse]
    page: int
    per_page: int
    total: int

