from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator, root_validator, Field
from .enums import Currency


def check_missing_fields(model_fields, values: dict, error_prefix: str = "") -> None:
    values_names = values.keys()
    missing_fields_names = list()
    for field in model_fields:
        print("{} {}".format(field, values_names))
        if field not in values_names:
            missing_fields_names.append(field)

    if len(missing_fields_names) != 0:
        raise ValueError("{} missing values: {}".format(error_prefix, " ".join(missing_fields_names)))


class Payment(BaseModel):
    created_at: datetime = Field()
    currency: Currency = Field()
    amount: int = Field(gt=0)
    description: str = Field(min_length=1)

    @validator('created_at')
    def validate_created_at(cls, v):
        """
        Validates created_at field, checks if payments date doesn't came from future
        """
        now_date = datetime.now(v.tzinfo)
        if v > now_date:
            raise ValueError("Payment cannot be from future!")
        return v

    @validator('currency')
    def validate_currency(cls, v):
        """
        Checks if currency is it on the list of supported currencies
        """
        if v not in Currency.__members__.keys():
            raise ValueError("Unsupported currency")
        return v


class PayByLink(Payment):
    bank: str = Field(min_length=1)


class DirectPayment(Payment):
    iban: str = Field(min_length=1)


class Card(Payment):
    cardholder_name: str = Field(min_length=1)
    cardholder_surname: str = Field(min_length=1)
    card_number: str = Field(min_length=15, max_length=16)


class ReportRequest(BaseModel):
    pay_by_link: Optional[List[PayByLink]] = Field(alias="pay_by_link", min_items=0)
    dp: Optional[List[DirectPayment]] = Field(alias="dp", min_items=0)
    card: Optional[List[Card]] = Field(alias="card", min_items=0)


class CustomerReportRequest(BaseModel):
    customer_id: str = Field(min_length=1)
    payments: 'ReportRequest' = Field()

