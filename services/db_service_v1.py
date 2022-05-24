from typing import List

from models import PaymentReport
from .IdbService import IDbService


class DbService1(IDbService):
    """
    Implementation of database using 'in memory way' can be easily replaced with 'real' dbservice without
    messing up with code.
    """

    def __init__(self):
        self.memory = dict()

    async def save_report(self, customer_id: str, report: List['PaymentReport']):
        self.memory[customer_id] = report

    async def get_customer_report(self, customer_id: str):
        return self.memory.get(customer_id, None)

    async def remove_customer_report(self, customer_id: str):
        self.memory.pop(customer_id)
