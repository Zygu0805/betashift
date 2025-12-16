"""
Airline Schemas
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field


class AirlineBase(BaseModel):
    """Base schema with common fields"""
    airline_code: str = Field(..., max_length=10, examples=["KE"])
    airline_name: str = Field(..., max_length=100, examples=["Korean Air"])
    color_code: str = Field(default="#808080", max_length=7, examples=["#0F4C81"])


class AirlineCreate(AirlineBase):
    """Schema for creating an airline"""
    pass


class AirlineResponse(AirlineBase):
    """Schema for airline response"""

    model_config = {"from_attributes": True}
