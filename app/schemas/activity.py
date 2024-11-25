# app/schemas/activity.py
from pydantic import BaseModel, Field
from typing import List, Optional
from .template import TemplateResponse

class ActivityBase(BaseModel):
    activityName: str = Field(..., alias="activityName")
    indexNo: Optional[str] = Field(None, alias="indexNo")
    description: Optional[str] = Field(None, alias="description")
    time: Optional[int] = Field(None, alias="time")
    repetitions: Optional[int] = Field(None, alias="repetitions")
    cadAdmins: Optional[int] = Field(None, alias="cadAdmins")
    cadCoords: Optional[int] = Field(None, alias="cadCoords")
    sum: Optional[int] = Field(None, alias="sum")
    wbsId: Optional[int] = Field(None, alias="wbsId")
    parentActivityId: Optional[int] = Field(None, alias="parentActivityId")
    templateId: Optional[int] = Field(None, alias="templateId")

    class Config:
        allow_population_by_field_name = True
        from_attributes = True

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    activityID: int = Field(..., alias="activityID")
    subActivities: List["ActivityResponse"] = Field([], alias="sub_activities")
    template: Optional[TemplateResponse] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        from_attributes = True

ActivityResponse.update_forward_refs()