from fastapi import APIRouter, exception_handlers
from models.requests import TestModel, PayByLink
from models import Card, Payment
from models.responses import PaymentInfo
from services import exchange_currency

router = APIRouter()


@router.get("/helloTest")
async def answer_hello():
    return {"message": "Test Router"}


@router.get("/bodyTest")
async def test_model(update: TestModel):
    return update


@router.get("/paymentTest")
async def hot_reload(update: PayByLink):
    return update


@router.get("/cardTest")
async def cardTest(update: Card):
    result = PaymentInfo.from_payment(update)
    print(update.currency)
    result.amount_in_pln = await exchange_currency(update)
    return result


@router.get("/nameTest")
async def nameTest(update: Payment):
    print(update.__fields__.keys())
    return {"message": "ok"}

