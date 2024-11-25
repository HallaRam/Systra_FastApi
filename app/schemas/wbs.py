# app/schemas/wbs_copy.py
from pydantic import BaseModel, Field
from typing import List, Optional
from .activity import ActivityResponse

class WbsBase(BaseModel):
    name: str = Field(..., alias="name")
    date: Optional[str] = Field(None, alias="date")
    cadAdmins: Optional[str] = None
    cadCoords: Optional[str] = None
    templateId: Optional[int] = None

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class WbsCreate(WbsBase):
    pass

class WbsResponse(WbsBase):
    wbsId: int = Field(..., alias="wbsId")
    activities: List[ActivityResponse] = []

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }