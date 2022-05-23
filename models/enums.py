from enum import Enum


class Currency(str, Enum):
    """
    All currently supported currencies, stored in Enum class easy to expand without messing up with code
    """
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    PLN = "PLN"


class PayMethods(Enum):
    """
    All currently supported payment methods, with ability to expand
    """
    PAYBYLINK = "pay_by_link"
    DIRECTPAYMENT = "dp"
    CARD = "card"
