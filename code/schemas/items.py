from typing import List

from pydantic import BaseModel, Field


class ItemsWorkflowSite(BaseModel):

    name: str
    url: str


class ItemsOutput(BaseModel):

    items_urls: List[str]


class ItemDetails(BaseModel):

    ref: str  # ID field

    # Localization
    city: str
    neighborhood: str

    # Classification
    category: str = Field(examples=["Casa", "Terreno"])
    application: str = Field(examples=["Residencial", "Comercial"])
    material: str = Field(examples=["Alvenaria", "Madeira"])
    value: float

    # Rooms count
    bedroom_count: int
    bathroom_count: int
    commom_room_count: int
    kitchen_count: int
    has_service_area: bool

    # Area
    total_area: float
    built_area: float
