# app/schemas/template.py
from pydantic import BaseModel, Field

class TemplateBase(BaseModel):
    templateName: str = Field(..., alias="templateName")

    class Config:
        allow_population_by_field_name = True
        from_attributes = True

class TemplateCreate(TemplateBase):
    pass

class TemplateResponse(TemplateBase):
    templateId: int = Field(..., alias="templateId")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        from_attributes = True