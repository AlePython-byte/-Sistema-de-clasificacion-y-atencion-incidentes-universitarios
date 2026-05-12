from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


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
    title: str = Field(
        ...,
        min_length=5,
        max_length=100,
        examples=["Broken classroom projector"],
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        examples=["The projector in room B-204 does not turn on."],
    )
    category: str = Field(..., min_length=1, max_length=80, examples=["Technology"])
    location: str = Field(
        ...,
        min_length=1,
        max_length=120,
        examples=["Building B, room 204"],
    )
    reported_by: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["student@example.edu"],
    )
    urgency_level: UrgencyLevel = Field(..., examples=["HIGH"])

    @field_validator("title", "description", "category", "location", "reported_by")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be empty.")
        return value.strip()


class IncidentUpdateStatusRequest(BaseModel):
    status: IncidentStatus = Field(..., examples=["IN_PROGRESS"])


class IncidentAssignRequest(BaseModel):
    assigned_to: str | None = Field(
        default=None,
        max_length=100,
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
    id: str = Field(..., examples=["9f7f7d37-1f46-4c6f-8a25-7a7c456f6ad9"])
    title: str = Field(..., examples=["Broken classroom projector"])
    description: str = Field(..., examples=["The projector in room B-204 does not turn on."])
    category: str = Field(..., examples=["Technology"])
    location: str = Field(..., examples=["Building B, room 204"])
    reported_by: str = Field(..., examples=["student@example.edu"])
    urgency_level: UrgencyLevel = Field(..., examples=["HIGH"])
    priority: IncidentPriority = Field(..., examples=["HIGH"])
    status: IncidentStatus = Field(..., examples=["OPEN"])
    assigned_to: str | None = Field(default=None, examples=["Maintenance Team"])
    created_at: datetime = Field(..., examples=["2026-05-12T10:30:00"])
