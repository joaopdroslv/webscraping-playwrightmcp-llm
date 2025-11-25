from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float


class ProductsOutput(BaseModel):
    products: List[Product]
