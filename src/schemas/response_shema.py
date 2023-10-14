from typing import TypeVar


T = TypeVar('T')


def create_response(detail: str | None = None, data: T | None = {}):
    if detail and data:
        return {"detail": detail, "data": data}
    if detail:
        return {"detail": detail}
    if data:
        return {"data": data}
