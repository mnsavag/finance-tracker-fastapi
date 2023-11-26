from fastapi import APIRouter

from .handlers import router


user_router = APIRouter()
user_router.include_router(router, prefix="/api/user", tags=["user"])
