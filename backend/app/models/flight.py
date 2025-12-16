"""
Flight Model
Stores arrival flight information
"""

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Flight(Base):
    """
    Flight table - Arrival flight information

    Columns:
        flight_id: Unique flight identifier (PK)
        airline: Airline code (FK to airlines table)
        flight_number: Flight number (e.g., "001", "123")
        scheduled_time: Scheduled arrival time
        pax_count: Number of passengers
        baggage_count: Number of baggage items
        aircraft_type: Aircraft type (e.g., "B737", "A380")
        created_at: Record creation timestamp
    """
    __tablename__ = "flights"

    flight_id = Column(String(20), primary_key=True)
    airline = Column(
        String(10),
        ForeignKey("airlines.airline_code"),
        nullable=False
    )
    flight_number = Column(String(10), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    pax_count = Column(Integer, default=0)
    baggage_count = Column(Integer, default=0)
    aircraft_type = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    airline_info = relationship("Airline", back_populates="flights")
    assignments = relationship("Assignment", back_populates="flight")

    def __repr__(self):
        return f"<Flight {self.flight_id}: {self.airline}{self.flight_number}>"
