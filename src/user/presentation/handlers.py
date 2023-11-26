from fastapi import APIRouter, Depends, status

from src.user.domain.schemas import UserCreate, UserOut
from src.user.domain.services import UserService


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(UserService)
) -> UserOut:
    return await user_service.add_user(user)
