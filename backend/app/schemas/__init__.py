"""
Schemas Package
Export all Pydantic schemas for easy import
"""

from app.schemas.airline import AirlineBase, AirlineCreate, AirlineResponse
from app.schemas.carousel import (
    CarouselBase,
    CarouselCreate,
    CarouselUpdate,
    CarouselResponse,
)
from app.schemas.flight import (
    FlightBase,
    FlightCreate,
    FlightResponse,
    FlightWithAirlineResponse,
)
from app.schemas.assignment import (
    AssignmentBase,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
    AssignmentWithDetailsResponse,
)

__all__ = [
    # Airline
    "AirlineBase",
    "AirlineCreate",
    "AirlineResponse",
    # Carousel
    "CarouselBase",
    "CarouselCreate",
    "CarouselUpdate",
    "CarouselResponse",
    # Flight
    "FlightBase",
    "FlightCreate",
    "FlightResponse",
    "FlightWithAirlineResponse",
    # Assignment
    "AssignmentBase",
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentResponse",
    "AssignmentWithDetailsResponse",
]
