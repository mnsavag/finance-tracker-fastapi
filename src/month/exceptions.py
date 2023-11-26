from fastapi import HTTPException, status


class InvalidDateFormatException(HTTPException):
    def __init__(self, detail) -> None:
        super().__init__(
            detail="Valid date format is year-month-day",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
