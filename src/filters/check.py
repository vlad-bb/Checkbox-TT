from decimal import Decimal
from typing import Optional, List
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from enum import Enum
from datetime import datetime

from sqlalchemy import Numeric

from src.database.models import Check


class PaymentTypeEnum(str, Enum):
    cash = "cash"
    cashless = "cashless"


class CheckFilter(Filter):
    payment_type: Optional[PaymentTypeEnum] = Field(None, alias="payment_type")
    created_at__gte: Optional[datetime] = Field(None, alias="createdAtFrom")
    created_at__lte: Optional[datetime] = Field(None, alias="createdAtTo")
    payment_amount__gte: Optional[Decimal] = Field(None, alias="paymentAmountFrom")
    payment_amount__lte: Optional[Decimal] = Field(None, alias="paymentAmountTo")

    class Constants(Filter.Constants):
        model = Check

    class Config:
        populate_by_name = True
