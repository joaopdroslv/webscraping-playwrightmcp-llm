from typing import List, Optional

from pydantic import BaseModel, Field


class ItemsWorkflowSite(BaseModel):

    name: str
    url: str


# Model structured output
class PageItemsOutput(BaseModel):

    items_urls: List[str]


# Model structured output
class ItemDetailsOutput(BaseModel):

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
    has_service_area: str = Field(examples=["Sim", "Não"])

    # Area
    total_area: float
    built_area: float


class ItemDetails(ItemDetailsOutput):

    site: Optional[str]
