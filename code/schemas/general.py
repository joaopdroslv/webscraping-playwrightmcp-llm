from code.schemas.pagination import Pagination
from typing import Optional

from pydantic import BaseModel


class Site(BaseModel):
    """Represents a site to be processed in the workflow."""

    name: str
    url: str

    homepage_snapshot: Optional[str] = None
    pagination: Optional[Pagination] = None

    # Relevant refs
    search_bar_ref: Optional[str] = None
