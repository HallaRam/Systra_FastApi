# app/routers/wbs_copy.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.database import get_db
from app.models.wbs_copy import WbsCopy
from app.models.activity_copy import ActivityCopy
from app.schemas.wbs_copy import WbsCopyCreate, WbsCopyResponse
from app.schemas.activity_copy import ActivityCopyResponse
from app.schemas.activity import ActivityCreate


router = APIRouter()

def filter_activity_copy(activities: List[ActivityCopy]) -> List[ActivityCopyResponse]:
    activity_map: Dict[int, ActivityCopyResponse] = {}
    root_activities: List[ActivityCopyResponse] = []

    # First pass: Create activity map and identify root activities
    for activity in activities:
        activity_response = ActivityCopyResponse.from_orm(activity)
        activity_map[activity.activityID] = activity_response
        if activity.parentActivityId is None or activity.parentActivityId == 0:
            root_activities.append(activity_response)
        activity_response.subActivities = []

    # Second pass: Build the tree structure
    for activity in activities:
        if activity.parentActivityId and activity.parentActivityId != 0:
            parent = activity_map.get(activity.parentActivityId)
            if parent:
                parent.subActivities.append(activity_map[activity.activityID])

    return root_activities

@router.get("/wbs-copy", response_model=List[WbsCopyResponse])
def get_wbs_copy_list(db: Session = Depends(get_db)):
    return db.query(WbsCopy).all()

@router.get("/wbs-copy/{wbs_id}", response_model=WbsCopyResponse)
def get_wbs_copy(wbs_id: int, db: Session = Depends(get_db)):
    wbs = db.query(WbsCopy).filter(WbsCopy.wbsId == wbs_id).first()
    if wbs is None:
        raise HTTPException(status_code=404, detail="WBS copy not found")
    wbs_response = WbsCopyResponse.from_orm(wbs)
    wbs_response.activities = filter_activity_copy(wbs.activities)
    
    # Update the sums in the database
    for activity in wbs.activities:
        db_activity = db.query(ActivityCopy).filter(ActivityCopy.activityID == activity.activityID).first()
        if db_activity:
            db_activity.sum = next((a.sum for a in wbs_response.activities if a.activityID == activity.activityID), 0)
    db.commit()
    
    return wbs_response

@router.get("/wbs-copy/{wbs_id}/activities", response_model=List[ActivityCopyResponse])
def get_wbs_copy_activities(wbs_id: int, db: Session = Depends(get_db)):
    activities = db.query(ActivityCopy).filter(ActivityCopy.wbsId == wbs_id).all()
    filtered_activities = filter_activity_copy(activities)
    
    # Update the sums in the database
    for activity in activities:
        db_activity = db.query(ActivityCopy).filter(ActivityCopy.activityID == activity.activityID).first()
        if db_activity:
            db_activity.sum = next((a.sum for a in filtered_activities if a.activityID == activity.activityID), 0)
    db.commit()
    
    return filtered_activities

@router.post("/wbs-copy", response_model=WbsCopyResponse)
def create_wbs_copy(wbs: WbsCopyCreate, db: Session = Depends(get_db)):
    db_wbs = WbsCopy(**wbs.dict(by_alias=True))
    db.add(db_wbs)
    db.commit()
    db.refresh(db_wbs)
    return db_wbs

@router.put("/wbs-copy/{wbs_id}", response_model=WbsCopyResponse)
def update_wbs_copy(wbs_id: int, wbs: WbsCopyCreate, db: Session = Depends(get_db)):
    db_wbs = db.query(WbsCopy).filter(WbsCopy.wbsId == wbs_id).first()
    if db_wbs is None:
        raise HTTPException(status_code=404, detail="WBS copy not found")
    for key, value in wbs.dict(by_alias=True).items():
        setattr(db_wbs, key, value)
    db.commit()
    db.refresh(db_wbs)
    return db_wbs

@router.delete("/wbs-copy/{wbs_id}", status_code=204)
def delete_wbs_copy(wbs_id: int, db: Session = Depends(get_db)):
    wbs = db.query(WbsCopy).filter(WbsCopy.wbsId == wbs_id).first()
    if wbs is None:
        raise HTTPException(status_code=404, detail="WBS copy not found")
    db.delete(wbs)
    db.commit()
    return {"ok": True}