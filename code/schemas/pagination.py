from typing import List

from pydantic import BaseModel


class PageItem(BaseModel):

    page_number: int
    page_url: str


class Pagination(BaseModel):

    total: int
    pages: List[PageItem]
