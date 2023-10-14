from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.v1.api import api_router as api_router_vOne


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)
app.include_router(api_router_vOne)
# uvicorn src.main:app --reload
