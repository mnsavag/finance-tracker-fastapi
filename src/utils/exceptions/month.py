from fastapi import HTTPException, status
from typing import Optional


class MonthNotFoundException(HTTPException):
    def __init__(self, user_id: Optional[int] = None) -> None:
        super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find current month of the user with id {user_id}.",
            )
