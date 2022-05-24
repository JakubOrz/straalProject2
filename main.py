import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse, PlainTextResponse

from routes import ClientsRouter
from pydantic import ValidationError

app = FastAPI()

app.include_router(
    router=ClientsRouter,
    prefix="",
    tags=['Reports']
)


@app.get("/")
async def main_page():
    """
    For tests if server is alive
    """
    return PlainTextResponse(status_code=200, content="OK")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    error_list = [error for error in exc.errors()]
    # error_list = ["{} : {}".format(error.get("loc")[-1], error.get("msg")) for error in exc.errors()]
    return JSONResponse(
        content={"errors": error_list},
        status_code=400
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
