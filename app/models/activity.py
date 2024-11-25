# app/models/activity.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"

    activityID = Column(Integer, primary_key=True, index=True)
    activityName = Column(String, index=True)
    indexNo = Column(String)
    description = Column(String)
    time = Column(Integer)
    repetitions = Column(Integer)
    cadAdmins = Column(Integer)
    cadCoords = Column(Integer)
    sum = Column(Integer)
    wbsId = Column(Integer, ForeignKey("wbs.wbsId"))
    parentActivityId = Column(Integer, ForeignKey("activities.activityID"))
    templateId = Column(Integer, ForeignKey("templates.templateId"))

    parent = relationship("Activity", remote_side=[activityID], back_populates="sub_activities")
    sub_activities = relationship("Activity", back_populates="parent")
    wbs = relationship("Wbs", back_populates="activities")
    template = relationship("Template", back_populates="activities")