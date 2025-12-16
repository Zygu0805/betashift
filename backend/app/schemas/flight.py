"""
Flight Schemas
Pydantic models for API request/response validation
"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.airline import AirlineResponse


class FlightBase(BaseModel):
    """Base schema with common fields"""
    flight_id: str = Field(..., max_length=20, examples=["KE001_20251215"])
    airline: str = Field(..., max_length=10, examples=["KE"])
    flight_number: str = Field(..., max_length=10, examples=["001"])
    scheduled_time: datetime = Field(..., examples=["2025-12-15T14:30:00"])
    pax_count: int = Field(default=0, ge=0, examples=[180])
    baggage_count: int = Field(default=0, ge=0, examples=[250])
    aircraft_type: str | None = Field(default=None, max_length=20, examples=["B737"])


class FlightCreate(FlightBase):
    """Schema for creating a flight"""
    pass


class FlightResponse(FlightBase):
    """Schema for flight response"""
    created_at: datetime

    model_config = {"from_attributes": True}


class FlightWithAirlineResponse(FlightResponse):
    """Schema for flight response with airline info"""
    airline_info: AirlineResponse | None = None
