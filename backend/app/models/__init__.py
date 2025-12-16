"""
Models Package
Export all models for easy import
"""

from app.models.airline import Airline
from app.models.carousel import Carousel
from app.models.flight import Flight
from app.models.assignment import Assignment

__all__ = [
    "Airline",
    "Carousel",
    "Flight",
    "Assignment",
]
