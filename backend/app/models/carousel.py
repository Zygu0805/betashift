"""
Carousel Model
Stores baggage carousel information
"""

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Carousel(Base):
    """
    Carousel table - Baggage carousel information

    Columns:
        carousel_id: Carousel identifier (PK, e.g., "C1", "C2", ... "C24")
        terminal: Terminal information (e.g., "T1", "T2")
        capacity: Carousel capacity
        is_active: Whether the carousel is currently operational
    """
    __tablename__ = "carousels"

    carousel_id = Column(String(10), primary_key=True)
    terminal = Column(String(10))
    capacity = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)

    # Relationships
    assignments = relationship("Assignment", back_populates="carousel")

    def __repr__(self):
        return f"<Carousel {self.carousel_id}>"
