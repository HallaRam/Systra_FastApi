import pytest
from pydantic import ValidationError
from app.schemas.activity import ActivityResponse, TemplateResponse

def test_activity_response_minimal():
    """Test creation of ActivityResponse with minimal valid data."""
    data = {
        "activityName": "Test Activity",
        "activityID": 1
    }
    response = ActivityResponse(**data)
    assert response.activityName == "Test Activity"
    assert response.activityID == 1
    assert response.subActivities == []  # Default value
    assert response.template is None  # Default value

def test_activity_response_with_optional_fields():
    """Test creation of ActivityResponse with optional fields."""
    data = {
        "activityName": "Detailed Activity",
        "activityID": 2,
        "indexNo": "001",
        "description": "This is a test description",
        "time": 120,
        "repetitions": 5,
        "cadAdmins": 10,
        "cadCoords": 2,
        "sum": 50,
        "wbsId": 1001,
        "parentActivityId": 0,
        "templateId": 42
    }
    response = ActivityResponse(**data)
    assert response.indexNo == "001"
    assert response.description == "This is a test description"
    assert response.time == 120
    assert response.templateId == 42

def test_activity_response_with_nested_subactivities():
    """Test recursive subActivities field with nested ActivityResponse."""
    data = {
        "activityName": "Parent Activity",
        "activityID": 1,
        "sub_activities": [
            {
                "activityName": "Child Activity 1",
                "activityID": 2
            },
            {
                "activityName": "Child Activity 2",
                "activityID": 3,
                "sub_activities": [
                    {
                        "activityName": "Grandchild Activity",
                        "activityID": 4
                    }
                ]
            }
        ]
    }
    response = ActivityResponse(**data)
    assert len(response.subActivities) == 2
    assert response.subActivities[0].activityName == "Child Activity 1"
    assert response.subActivities[1].subActivities[0].activityName == "Grandchild Activity"

def test_activity_response_with_template():
    """Test handling of optional TemplateResponse field."""
    template_data = {
        "templateID": 10,
        "templateName": "Example Template"
    }
    data = {
        "activityName": "Activity with Template",
        "activityID": 1,
        "template": template_data
    }
    response = ActivityResponse(**data)
    assert response.template is not None
    assert response.template.templateID == 10
    assert response.template.templateName == "Example Template"

def test_activity_response_validation_errors():
    """Test validation errors for missing required fields."""
    # Missing activityName and activityID
    data = {"description": "This should fail"}
    with pytest.raises(ValidationError):
        ActivityResponse(**data)

def test_activity_response_alias_handling():
    """Test that alias fields work correctly."""
    data = {
        "activityName": "Aliased Activity",
        "activityID": 1,
        "sub_activities": [
            {"activityName": "Nested Activity", "activityID": 2}
        ]
    }
    response = ActivityResponse(**data)
    assert response.activityID == 1
    assert response.subActivities[0].activityID == 2
