from typing import Any, Dict, Optional
from fastapi import HTTPException, status

from src.models.user import User

class UserExistException(HTTPException):
    def __init__(self, id: Optional[int] = None, mail: Optional[str] = None) -> None:
        detail = ""
        if id:
            detail=f"User with this id {id} already exists."
        elif mail:
            detail=f"User with this mail {mail} already exists."
        
        if detail:
            super().__init__(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=detail,
                )

class UserNotFoundException(HTTPException):
    def __init__(self, id: Optional[int] = None) -> None:
        super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Unable to find the Telegram user with id {id}.",
            )
