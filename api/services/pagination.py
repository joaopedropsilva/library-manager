from typing import Any
import math

from pydantic import BaseModel


class MemoryPaginatedResponse(BaseModel):
    total_items: int
    page_items: list[Any]
    page: int
    total_pages: int


def paginate_response(items: list[Any], skip: int, limit: int) -> MemoryPaginatedResponse:
    return MemoryPaginatedResponse(
        total_items=len(items),
        page_items=items[skip:skip + limit],
        page=skip // limit,
        total_pages=math.ceil(len(items) / limit)
    )
