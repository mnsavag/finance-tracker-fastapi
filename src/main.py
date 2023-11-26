from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from user.presentation.router import user_router


app = FastAPI()

app.include_router(user_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        raise Response("Internal Server Error", status_code=500)


app.middleware('http')(catch_exceptions_middleware)



# uvicorn src.main:app --reload