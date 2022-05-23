from datetime import datetime
from typing import List

from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from models import ReportRequestData, PayByLink, DirectPayment, Card, PaymentInfo, PayMethods
from services import exchange_currency

router = APIRouter()


@router.get("/")
async def main_page(body: ReportRequestData):
    resultList: List[PaymentInfo] = list()

    for payment_by_link in body.pay_by_link:
        newPaymentSummary = PaymentInfo.from_payment(payment_by_link)
        newPaymentSummary.amount_in_pln = await exchange_currency(payment_by_link)
        newPaymentSummary.type = PayMethods.PAYBYLINK
        newPaymentSummary.payment_mean = "bank"
        resultList.append(newPaymentSummary)

    for direct_payment in body.dp:
        newPaymentSummary = PaymentInfo.from_payment(direct_payment)
        newPaymentSummary.amount_in_pln = await exchange_currency(direct_payment)
        newPaymentSummary.type = PayMethods.DIRECTPAYMENT
        newPaymentSummary.payment_mean = "iban"
        resultList.append(newPaymentSummary)

    for card_payment in body.card:
        newPaymentSummary = PaymentInfo.from_payment(card_payment)
        newPaymentSummary.amount_in_pln = await exchange_currency(card_payment)
        newPaymentSummary.type = PayMethods.CARD
        newPaymentSummary.payment_mean = "{} {} {}".format(
            card_payment.cardholder_name,
            card_payment.cardholder_surname,
            "{}{}{}".format(
                card_payment.card_number[0:4],
                "*" * (len(card_payment.card_number) - 8),
                card_payment.card_number[-4:]
            )
        )
        resultList.append(newPaymentSummary)

    return sorted(resultList, key=lambda x: datetime.strptime(x.date, '%Y-%m-%dT%H:%M:%SZ').timestamp())


@router.get("/count")
async def main_page(body: ReportRequestData):
    for payment in body.__fields__.keys():
        print(getattr(body, payment, None))
    return PlainTextResponse(content="ok", status_code=200)
