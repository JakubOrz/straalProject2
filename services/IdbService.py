from typing import List

from models import PaymentReport


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class IDbService(metaclass=SingletonMeta):

    async def save_report(self, customer_id: str, report: List['PaymentReport']):
        pass

    async def get_customer_report(self, customer_id: str):
        pass

    async def remove_customer_report(self, customer_id: str):
        pass
