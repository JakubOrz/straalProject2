import random
import string
import pytest
from datetime import datetime
from services import IDbService, DbService
from models import PaymentReport, PayMethods, Currency


@pytest.mark.asyncio
async def test_not_existing_clients():
    random_customer_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    db_service: IDbService = DbService()
    try:
        await db_service.get_customer_report(random_customer_id)
    except Exception:
        assert False, f"Service should not crash even if customer does not exists"


@pytest.mark.asyncio
async def test_save_and_load_data():
    payments = [
        PaymentReport(
            date=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            type=PayMethods.PAYBYLINK.name,
            payment_mean="bank",
            description="No why",
            amount=69420,
            currency=Currency.PLN.name,
            amount_in_pln=69420
        )
    ]
    random_customer_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(13))
    db_service: IDbService = DbService()

    try:
        await db_service.save_report(customer_id=random_customer_id, report=payments)
    except Exception:
        assert False, f"Service should not crash while saving data"

    try:
        loaded_raport = await db_service.get_customer_report(random_customer_id)
    except Exception:
        assert False, "Service should not crash while loading data"

    assert loaded_raport == payments, "Data loaded from db should not be changed"

    # Clean db after testing
    await db_service.remove_customer_report(random_customer_id)
