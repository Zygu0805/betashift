"""
Carousel Schemas
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field


class CarouselBase(BaseModel):
    """Base schema with common fields"""
    carousel_id: str = Field(..., max_length=10, examples=["C1"])
    terminal: str | None = Field(default=None, max_length=10, examples=["T1"])
    capacity: int = Field(default=100, ge=0, examples=[100])
    is_active: bool = Field(default=True)


class CarouselCreate(CarouselBase):
    """Schema for creating a carousel"""
    pass


class CarouselUpdate(BaseModel):
    """Schema for updating a carousel (all fields optional)"""
    terminal: str | None = None
    capacity: int | None = None
    is_active: bool | None = None


class CarouselResponse(CarouselBase):
    """Schema for carousel response"""

    model_config = {"from_attributes": True}
