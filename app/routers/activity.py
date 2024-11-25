# app/routers/activity.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.database import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityResponse
from app.models.activity_copy import ActivityCopy
from app.schemas.activity_copy import ActivityCopyResponse, ActivityCopyRequest
from app.models.template import Template

router = APIRouter()

@router.get("/activities", response_model=List[ActivityResponse])
def get_activities(db: Session = Depends(get_db)):
    activities = db.query(Activity).all()
    activity_responses = [ActivityResponse.from_orm(activity) for activity in activities]
    return activity_responses

@router.get("/activities/suggestions", response_model=List[str])
def get_activity_name_suggestions(db: Session = Depends(get_db)):
    return db.query(Activity.activityName).filter(Activity.parentActivityId == None).distinct().all()

@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.activityID == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.post("/activities", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = Activity(**activity.dict(by_alias=True))
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.put("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = db.query(Activity).filter(Activity.activityID == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    for key, value in activity.dict(by_alias=True).items():
        setattr(db_activity, key, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.delete("/activities/{activity_id}", status_code=204)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.activityID == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(activity)
    db.commit()
    return {"ok": True}
    

@router.post("/activities/copy-by-wbs/{wbs_id}", response_model=List[ActivityCopyResponse])
def copy_activities_by_wbs(
    wbs_id: int, 
    copy_request: ActivityCopyRequest, 
    db: Session = Depends(get_db)
):
    # Get all activities for the given WBS
    activities = db.query(Activity).filter(Activity.wbsId == wbs_id).all()
    
    if not activities:
        raise HTTPException(status_code=404, detail="No activities found for this WBS")

    # Handle template logic
    template_id = None
    if copy_request.templateId:
        # Verify template exists
        template = db.query(Template).filter(Template.templateId == copy_request.templateId).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        template_id = copy_request.templateId
    elif copy_request.templateName:
        # Create new template
        new_template = Template(templateName=copy_request.templateName)
        db.add(new_template)
        db.flush()  # This assigns an ID to the new template
        template_id = new_template.templateId
    else:
        raise HTTPException(
            status_code=400, 
            detail="Either templateId or templateName must be provided"
        )
    
    # Dictionary to store mapping between old and new activity IDs
    id_mapping = {}
    copied_activities = []
    
    # First pass: Create all activities without parent relationships
    for activity in activities:
        activity_copy_data = {
            "activityName": activity.activityName,
            "indexNo": activity.indexNo,
            "description": activity.description,
            "time": activity.time,
            "repetitions": activity.repetitions,
            "cadAdmins": activity.cadAdmins,
            "cadCoords": activity.cadCoords,
            "sum": activity.sum,
            # "wbsId": activity.wbsId,
            "templateId": template_id  # Use the new or existing template ID
        }
        
        activity_copy = ActivityCopy(**activity_copy_data)
        db.add(activity_copy)
        db.flush()  # This assigns an ID to the new activity
        
        # Store the mapping between old and new IDs
        id_mapping[activity.activityID] = activity_copy.activityID
        copied_activities.append(activity_copy)
    
    # Second pass: Update parent relationships using the id_mapping
    for activity, copied_activity in zip(activities, copied_activities):
        if activity.parentActivityId:
            new_parent_id = id_mapping.get(activity.parentActivityId)
            if new_parent_id:
                copied_activity.parentActivityId = new_parent_id
    
    db.commit()
    
    return copied_activities