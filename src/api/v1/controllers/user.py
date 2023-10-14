from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException

from src.schemas.user_shema import IUserCreate, IUserDataRead
from src.schemas.response_shema import create_response

from src.repository.user import UserRepository
from src.services.user import UserService

from src.deps.services import get_user_service


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: IUserCreate,
    user_service: UserService = Depends(UserService)
):
    await user_service.add_user(new_user)
    return create_response(detail="User created")
