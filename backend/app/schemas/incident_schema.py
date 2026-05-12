from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UrgencyLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class IncidentPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentCreateRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Broken classroom projector",
                    "description": "The projector in room B-204 does not turn on during class.",
                    "category": "Technology",
                    "location": "Building B, room 204",
                    "reported_by": "teacher@example.edu",
                    "urgency_level": "HIGH",
                }
            ]
        }
    )

    title: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="Short title that summarizes the reported incident.",
        examples=["Broken classroom projector"],
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Detailed explanation of what happened or what needs attention.",
        examples=["The projector in room B-204 does not turn on."],
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=80,
        description="General incident category.",
        examples=["Technology"],
    )
    location: str = Field(
        ...,
        min_length=1,
        max_length=120,
        description="Campus location where the incident occurred.",
        examples=["Building B, room 204"],
    )
    reported_by: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Person or group that reported the incident.",
        examples=["student@example.edu"],
    )
    urgency_level: UrgencyLevel = Field(
        ...,
        description="Initial urgency level reported by the user.",
        examples=["HIGH"],
    )

    @field_validator("title", "description", "category", "location", "reported_by")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be empty.")
        return value.strip()


class IncidentUpdateStatusRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"status": "IN_PROGRESS"}]})

    status: IncidentStatus = Field(
        ...,
        description="New lifecycle status for the incident.",
        examples=["IN_PROGRESS"],
    )


class IncidentAssignRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"assigned_to": "Maintenance Team"}]})

    assigned_to: str | None = Field(
        default=None,
        max_length=100,
        description="Responsible person or team assigned to handle the incident.",
        examples=["Maintenance Team"],
    )

    @field_validator("assigned_to")
    @classmethod
    def validate_assigned_to_not_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Assigned person or team cannot be empty.")
        return value.strip()


class IncidentResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "9f7f7d37-1f46-4c6f-8a25-7a7c456f6ad9",
                    "title": "Broken classroom projector",
                    "description": "The projector in room B-204 does not turn on.",
                    "category": "Technology",
                    "location": "Building B, room 204",
                    "reported_by": "student@example.edu",
                    "urgency_level": "HIGH",
                    "priority": "HIGH",
                    "status": "OPEN",
                    "assigned_to": None,
                    "created_at": "2026-05-12T10:30:00Z",
                }
            ]
        }
    )

    id: str = Field(
        ...,
        description="Unique incident identifier.",
        examples=["9f7f7d37-1f46-4c6f-8a25-7a7c456f6ad9"],
    )
    title: str = Field(..., description="Incident title.", examples=["Broken classroom projector"])
    description: str = Field(
        ...,
        description="Detailed incident description.",
        examples=["The projector in room B-204 does not turn on."],
    )
    category: str = Field(..., description="Incident category.", examples=["Technology"])
    location: str = Field(..., description="Incident location.", examples=["Building B, room 204"])
    reported_by: str = Field(
        ...,
        description="Person or group that reported the incident.",
        examples=["student@example.edu"],
    )
    urgency_level: UrgencyLevel = Field(..., description="Reported urgency level.", examples=["HIGH"])
    priority: IncidentPriority = Field(..., description="Calculated priority.", examples=["HIGH"])
    status: IncidentStatus = Field(..., description="Current incident status.", examples=["OPEN"])
    assigned_to: str | None = Field(
        default=None,
        description="Responsible person or team assigned to the incident.",
        examples=["Maintenance Team"],
    )
    created_at: datetime = Field(
        ...,
        description="UTC date and time when the incident was created.",
        examples=["2026-05-12T10:30:00Z"],
    )
