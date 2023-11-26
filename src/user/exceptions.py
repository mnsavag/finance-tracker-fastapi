from typing import Optional
from fastapi import HTTPException, status


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

class MonthNotFoundException(HTTPException):
    def __init__(self, user_id: Optional[int] = None) -> None:
        super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find current month of the user with id {user_id}.",
            )
