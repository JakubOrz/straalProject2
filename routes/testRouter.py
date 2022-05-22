from fastapi import APIRouter, exception_handlers
from models.requests import TestModel


router = APIRouter()


@router.get("/helloTest")
async def answer_hello():
    return {"message": "Test Router"}


@router.get("/bodyTest")
async def test_model(update: TestModel):
    return update


@router.get("/test2")
async def hot_reload():
    return "Hot reloaded"
