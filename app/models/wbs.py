# app/models/wbs.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Wbs(Base):
    __tablename__ = "wbs"

    wbsId = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String)
    cadAdmins = Column(String, nullable=True)
    cadCoords = Column(String, nullable=True)
    templateId = Column(Integer, ForeignKey("templates.templateId"), nullable=True)

    activities = relationship("Activity", back_populates="wbs")
    # activities_copy = relationship("ActivityCopy", back_populates="wbs")
    template = relationship("Template", back_populates="wbs_list")