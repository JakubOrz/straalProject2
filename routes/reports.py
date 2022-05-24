from typing import List

from fastapi import APIRouter
from models import ReportRequestData, CustomerReport, CustomerReportRequest
from services import exchange_currency, preprare_report
from services import DbService, IDbService
from starlette.responses import PlainTextResponse

router = APIRouter()


@router.post("/report")
async def report(body: ReportRequestData):
    return await preprare_report(body)


@router.post("/customer-report")
async def customer_report(body: CustomerReportRequest):
    customer_payment_report = await preprare_report(body.payments)

    dbservice: IDbService = DbService()
    await dbservice.save_report(customer_id=body.customer_id, report=customer_payment_report)
    return CustomerReport(
        customer_id=body.customer_id,
        report=customer_payment_report
    )


@router.get("/customer-report/{customer_id}")
async def customer_report(customer_id: str):
    dbservice: IDbService = DbService()
    c_report = await dbservice.get_customer_report(customer_id)
    if c_report is None:
        return PlainTextResponse(status_code=404)
    return CustomerReport(
        customer_id=customer_id,
        report=c_report
    )
