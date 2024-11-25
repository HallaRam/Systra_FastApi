# app/schemas/wbs_copy.py
from pydantic import BaseModel, Field
from typing import List, Optional
from .activity_copy import ActivityCopyResponse

class WbsCopyBase(BaseModel):
    name: str = Field(..., alias="name")
    date: Optional[str] = Field(None, alias="date")
    templateId: Optional[int] = None
    
    class Config:
        allow_population_by_field_name = True
        from_attributes = True

class WbsCopyCreate(WbsCopyBase):
    pass

class WbsCopyResponse(WbsCopyBase):
    wbsId: int = Field(..., alias="wbsId")
    activities: List[ActivityCopyResponse] = []

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        from_attributes = True