from typing import List

from pydantic import BaseModel
from datetime import datetime, timezone
from .requests import Payment


class PaymentReport(BaseModel):

    date: str = None
    type: str = None
    payment_mean: str = None
    description: str = None
    amount: int = 0
    currency: str = None
    amount_in_pln: int = 0

    @classmethod
    def from_payment(cls, payment: Payment) -> 'PaymentReport':
        return cls(
            date=payment.created_at.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            description=payment.description,
            amount=payment.amount,
            currency=payment.currency
        )


class CustomerReport(BaseModel):
    customer_id: str = None
    report: List['PaymentReport'] = None
