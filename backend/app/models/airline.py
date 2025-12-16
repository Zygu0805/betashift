"""
Airline Model
Stores airline information including display colors
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class Airline(Base):
    """
    Airline table - Airline information

    Columns:
        airline_code: Airline code (PK, e.g., "KE", "OZ", "7C")
        airline_name: Full airline name (e.g., "Korean Air", "Asiana Airlines")
        color_code: UI display color in hex format (e.g., "#0F4C81")
    """
    __tablename__ = "airlines"

    airline_code = Column(String(10), primary_key=True)
    airline_name = Column(String(100), nullable=False)
    color_code = Column(String(7), default="#808080")

    # Relationships
    flights = relationship("Flight", back_populates="airline_info")

    def __repr__(self):
        return f"<Airline {self.airline_code}: {self.airline_name}>"
