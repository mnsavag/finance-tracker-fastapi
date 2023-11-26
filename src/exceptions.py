from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail) -> None:
        super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

class IdNotFoundException(HTTPException):
    def __init__(self, model, id: int = None) -> None:
        if id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the {model.__name__} with id {id}."
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} id not found."
        )

class UnprocessableEntityException(HTTPException):
    def __init__(self, detail) -> None:
        super().__init__(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=detail,
            )
