from fastapi import APIRouter

from src.api.v1.controllers import (
    user, month
)

api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/user")

api_router.include_router(month.router, prefix="/api/month")
