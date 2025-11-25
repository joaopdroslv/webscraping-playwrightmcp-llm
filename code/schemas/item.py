from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    ref: str
    name: str


class ItemsOutput(BaseModel):
    items: List[Item]
