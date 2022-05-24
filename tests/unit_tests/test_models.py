import datetime
import pytest

from models import Payment
from pydantic import ValidationError


def test_payment_model_1():
    try:
        payment1 = Payment(
            created_at=datetime.datetime.now(),
            currency="EUR",
            amount=100,
            description="Test number 1"
        )
    except Exception:
        assert False, f"Payment model throw exception despite correct data"


def test_payment_model_2():
    with pytest.raises(ValidationError) as exception:
        payment2 = Payment(
            created_at=datetime.datetime.now(),
            currency="EUR",
            amount=-100,
            description="Test number 2"
        )


def test_payment_model_3():
    with pytest.raises(ValidationError) as exception:
        payment3 = Payment(
            created_at=datetime.datetime.now() + datetime.timedelta(days=10),
            currency="XXX",
            amount=4300,
            description="Test number 3"
        )
    assert "value is not a valid enumeration member" in str(exception.value)
    assert "Payment cannot be from future" in str(exception.value.errors())


def test_payment_model_4():
    with pytest.raises(ValidationError) as exception:
        payment4 = Payment(
            currency="PLN",
            amount=432,
            description="Test number 4"
        )
    assert "field required" in str(exception.value)
