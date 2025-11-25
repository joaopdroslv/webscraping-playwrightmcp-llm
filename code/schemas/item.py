from typing import List

from pydantic import BaseModel, Field


class Item(BaseModel):
    url: str
    name: str


class ItemsOutput(BaseModel):
    items: List[Item]


class ItemDetailed(BaseModel):
    ref: str
    city: str
    neighborhood: str
    category: str = Field(examples=["Casa", "Terreno"])
    application: str = Field(examples=["Residencial", "Comercial"])
    value: float

    bedroom_count: int
    bathroom_count: int
    commom_room_count: int
    kitchen_count: int
    has_service_area: bool

    total_area: float
    built_area: float
    material: str = Field(examples=["Alvenaria", "Madeira"])


class ItemsDetailedOutput(BaseModel):
    items_detailed: List[Item]
