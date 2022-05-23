import requests
from models import Currency, Payment
import math


async def exchange_currency(payment: Payment) -> int:
    currency = payment.currency
    amount = payment.amount
    date = payment.created_at

    if currency == Currency.PLN:
        return amount

    url = f"http://api.nbp.pl/api/exchangerates/rates/a/" \
          f"{currency.lower()}/{date.strftime('%Y-%m-%d')}/?format=json"
    result = requests.get(url=url).json()
    exchange_mid_rate = result['rates'][0]['mid']
    return math.floor(amount * exchange_mid_rate)
