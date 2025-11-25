from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float


class ProductList(BaseModel):
    products: List[Product]
