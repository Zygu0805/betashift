"""
Assignment Model
Stores carousel assignment records for flights
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Assignment(Base):
    """
    Assignment table - Carousel assignment records

    Columns:
        assignment_id: Auto-increment primary key
        flight_id: Flight identifier (FK to flights table)
        carousel_id: Carousel identifier (FK to carousels table)
        start_time: Carousel occupation start time
        end_time: Carousel occupation end time
        assignment_type: Assignment type ("MANUAL" or "AI")
        created_at: Record creation timestamp
        updated_at: Record update timestamp
    """
    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(
        String(20),
        ForeignKey("flights.flight_id"),
        nullable=False
    )
    carousel_id = Column(
        String(10),
        ForeignKey("carousels.carousel_id"),
        nullable=False
    )
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    assignment_type = Column(String(10), default="MANUAL")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    flight = relationship("Flight", back_populates="assignments")
    carousel = relationship("Carousel", back_populates="assignments")

    def __repr__(self):
        return f"<Assignment {self.assignment_id}: {self.flight_id} -> {self.carousel_id}>"
