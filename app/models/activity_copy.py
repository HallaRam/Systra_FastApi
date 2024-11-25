# app/models/activity_copy.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ActivityCopy(Base):
    __tablename__ = "activities_copy"

    activityID = Column(Integer, primary_key=True, index=True)
    activityName = Column(String, index=True)
    indexNo = Column(String)
    description = Column(String)
    time = Column(Integer)
    repetitions = Column(Integer)
    cadAdmins = Column(Integer)
    cadCoords = Column(Integer)
    sum = Column(Integer)
    # wbsId = Column(Integer, ForeignKey("wbs.wbsId"))
    parentActivityId = Column(Integer, ForeignKey("activities_copy.activityID"))
    templateId = Column(Integer, ForeignKey("templates.templateId"))

    parent = relationship("ActivityCopy", remote_side=[activityID], back_populates="sub_activities")
    sub_activities = relationship("ActivityCopy", back_populates="parent")
    # wbs = relationship("WbsCopy", back_populates="activities")
    template = relationship("Template", back_populates="activities_copy")