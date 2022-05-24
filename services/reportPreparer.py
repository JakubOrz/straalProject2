
from datetime import datetime
from typing import List

from models import PaymentReport, PayMethods
from services import exchange_currency
from models import ReportRequestData, PaymentReport


async def preprare_report(body: ReportRequestData) -> List['PaymentReport']:
    resultList: List[PaymentReport] = list()

    if body.pay_by_link is not None:
        for payment_by_link in body.pay_by_link:
            newPaymentSummary = PaymentReport.from_payment(payment_by_link)
            newPaymentSummary.amount_in_pln = await exchange_currency(payment_by_link)
            newPaymentSummary.type = PayMethods.PAYBYLINK
            newPaymentSummary.payment_mean = "bank"
            resultList.append(newPaymentSummary)

    if body.dp is not None:
        for direct_payment in body.dp:
            newPaymentSummary = PaymentReport.from_payment(direct_payment)
            newPaymentSummary.amount_in_pln = await exchange_currency(direct_payment)
            newPaymentSummary.type = PayMethods.DIRECTPAYMENT
            newPaymentSummary.payment_mean = direct_payment.iban
            resultList.append(newPaymentSummary)

    if body.card is not None:
        for card_payment in body.card:
            newPaymentSummary = PaymentReport.from_payment(card_payment)
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
