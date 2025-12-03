from typing import Optional
from pydantic import BaseModel

from code.schemas.pagination import Pagination


class TargetSite(BaseModel):
    """Represents a site to be processed in the workflow."""

    name: str
    url: str

    homepage_snapshot: Optional[str] = None
    pagination: Optional[Pagination] = None
