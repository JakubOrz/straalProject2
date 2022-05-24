import datetime
import random
from random import Random

import pytest

from models import Payment
from services import exchange_currency


@pytest.mark.asyncio
async def test_exchange_1():
    payment1 = Payment(
        created_at=datetime.datetime(year=2021, month=5, day=13),
        currency="EUR",
        amount=3000,
        description="Testing exchange power"
    )
    ammount_pln = await exchange_currency(payment1)
    assert ammount_pln == 13494


@pytest.mark.asyncio
async def test_exchange_2():
    payment2 = Payment(
        created_at=datetime.datetime(year=2021, month=5, day=14),
        currency="USD",
        amount=599,
        description="Test 2"
    )
    ammount_pln = await exchange_currency(payment2)
    assert ammount_pln == 2219


@pytest.mark.asyncio
async def test_exchange_3():
    random_amount = random.randint(1, 3000)
    payment3 = Payment(
        created_at=datetime.datetime(year=2020, month=2, day=14),
        currency="PLN",
        amount=random_amount,
        description="Test 3"
    )
    ammount_pln = await exchange_currency(payment3)
    assert ammount_pln == random_amount
