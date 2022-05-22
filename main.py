import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from routes import ClientsRouter, TestRouter
from pydantic import ValidationError

app = FastAPI()

app.include_router(
    router=ClientsRouter,
    prefix="",
    tags=['Payments']
)

app.include_router(
    router=TestRouter,
    prefix="/testRouter",
    tags=['tester']
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    error_list = [error.get("msg") for error in exc.errors()]
    return JSONResponse(
        content={"errors": error_list},
        status_code=400
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
