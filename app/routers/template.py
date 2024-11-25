# app/routers/template.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateResponse

router = APIRouter()

@router.post("/templates", response_model=TemplateResponse)
def create_template(template: TemplateCreate, db: Session = Depends(get_db)):
    db_template = Template(**template.dict(by_alias=True))
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.get("/templates", response_model=List[TemplateResponse])
def get_templates(db: Session = Depends(get_db)):
    return db.query(Template).all()

@router.get("/templates/{template_id}", response_model=TemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(Template).filter(Template.templateId == template_id).first()
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put("/templates/{template_id}", response_model=TemplateResponse)
def update_template(template_id: int, template: TemplateCreate, db: Session = Depends(get_db)):
    db_template = db.query(Template).filter(Template.templateId == template_id).first()
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    for key, value in template.dict(by_alias=True).items():
        setattr(db_template, key, value)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.delete("/templates/{template_id}", status_code=204)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(Template).filter(Template.templateId == template_id).first()
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(template)
    db.commit()
    return {"ok": True}