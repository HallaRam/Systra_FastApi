# app/routers/activity_copy.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.database import get_db
from app.models.activity_copy import ActivityCopy
from app.schemas.activity_copy import ActivityCopyCreate, ActivityCopyResponse

router = APIRouter()

@router.get("/activities-copy", response_model=List[ActivityCopyResponse])
def get_activities_copy(db: Session = Depends(get_db)):
    activities = db.query(ActivityCopy).all()
    activity_responses = [ActivityCopyResponse.from_orm(activity) for activity in activities]
    return activity_responses

@router.get("/activities-copy/suggestions", response_model=List[str])
def get_activity_copy_name_suggestions(db: Session = Depends(get_db)):
    return db.query(ActivityCopy.activityName).filter(ActivityCopy.parentActivityId == None).distinct().all()

@router.get("/activities-copy/{activity_id}", response_model=ActivityCopyResponse)
def get_activity_copy(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(ActivityCopy).filter(ActivityCopy.activityID == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity copy not found")
    return activity

@router.post("/activities-copy", response_model=ActivityCopyResponse)
def create_activity_copy(activity: ActivityCopyCreate, db: Session = Depends(get_db)):
    db_activity = ActivityCopy(**activity.dict(by_alias=True))
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.put("/activities-copy/{activity_id}", response_model=ActivityCopyResponse)
def update_activity_copy(activity_id: int, activity: ActivityCopyCreate, db: Session = Depends(get_db)):
    db_activity = db.query(ActivityCopy).filter(ActivityCopy.activityID == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity copy not found")
    for key, value in activity.dict(by_alias=True).items():
        setattr(db_activity, key, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.delete("/activities-copy/{activity_id}", status_code=204)
def delete_activity_copy(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(ActivityCopy).filter(ActivityCopy.activityID == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity copy not found")
    db.delete(activity)
    db.commit()
    return {"ok": True}
    

# Add endpoint to get copied activities by template
@router.get("/activities-copy/by-template/{template_id}", response_model=List[ActivityCopyResponse])
def get_copied_activities_by_template(template_id: int, db: Session = Depends(get_db)):
    activities = db.query(ActivityCopy).filter(ActivityCopy.templateId == template_id).all()
    
    if not activities:
        raise HTTPException(
            status_code=404, 
            detail="No copied activities found for this template"
        )
    
    def filter_activity(activities: List[ActivityCopy]) -> List[ActivityCopyResponse]:
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

    return filter_activity(activities)