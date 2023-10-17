from fastapi import APIRouter, Depends, status

from src.schemas.user_shema import IUserCreate
from src.schemas.response_shema import create_response

from src.services.user import UserService


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: IUserCreate,
    user_service: UserService = Depends(UserService)
):
    await user_service.add_user(new_user)
    return create_response(detail="User created")
