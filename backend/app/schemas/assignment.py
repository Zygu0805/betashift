"""
Assignment Schemas
Pydantic models for API request/response validation
"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.flight import FlightResponse
from app.schemas.carousel import CarouselResponse


class AssignmentBase(BaseModel):
    """Base schema with common fields"""
    flight_id: str = Field(..., max_length=20, examples=["KE001_20251215"])
    carousel_id: str = Field(..., max_length=10, examples=["C1"])
    start_time: datetime = Field(..., examples=["2025-12-15T14:30:00"])
    end_time: datetime = Field(..., examples=["2025-12-15T15:00:00"])
    assignment_type: str = Field(default="MANUAL", max_length=10, examples=["MANUAL"])


class AssignmentCreate(AssignmentBase):
    """Schema for creating an assignment"""
    pass


class AssignmentUpdate(BaseModel):
    """Schema for updating an assignment (all fields optional)"""
    carousel_id: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    assignment_type: str | None = None


class AssignmentResponse(AssignmentBase):
    """Schema for assignment response"""
    assignment_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssignmentWithDetailsResponse(AssignmentResponse):
    """Schema for assignment response with flight and carousel info"""
    flight: FlightResponse | None = None
    carousel: CarouselResponse | None = None
