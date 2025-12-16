"""
Airlines API Router
CRUD operations for airline management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Airline
from app.schemas import AirlineCreate, AirlineResponse

router = APIRouter()


@router.get("/", response_model=list[AirlineResponse])
def get_airlines(db: Session = Depends(get_db)):
    """
    Get all airlines with their color codes.
    Used for UI display (flight bar colors).
    """
    airlines = db.query(Airline).all()
    return airlines


@router.get("/{airline_code}", response_model=AirlineResponse)
def get_airline(airline_code: str, db: Session = Depends(get_db)):
    """Get a specific airline by code."""
    airline = db.query(Airline).filter(Airline.airline_code == airline_code).first()
    if not airline:
        raise HTTPException(status_code=404, detail="Airline not found")
    return airline


@router.post("/", response_model=AirlineResponse, status_code=201)
def create_airline(airline: AirlineCreate, db: Session = Depends(get_db)):
    """Create a new airline."""
    # Check if airline already exists
    existing = db.query(Airline).filter(
        Airline.airline_code == airline.airline_code
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Airline already exists")

    db_airline = Airline(**airline.model_dump())
    db.add(db_airline)
    db.commit()
    db.refresh(db_airline)
    return db_airline


@router.post("/init", response_model=list[AirlineResponse], status_code=201)
def init_airlines(db: Session = Depends(get_db)):
    """
    Initialize default airlines with their brand colors.
    Call this once to set up initial data.
    """
    default_airlines = [
        {"airline_code": "KE", "airline_name": "Korean Air", "color_code": "#0F4C81"},
        {"airline_code": "OZ", "airline_name": "Asiana Airlines", "color_code": "#C9252D"},
        {"airline_code": "7C", "airline_name": "Jeju Air", "color_code": "#FF6600"},
        {"airline_code": "TW", "airline_name": "T'way Air", "color_code": "#E60012"},
        {"airline_code": "LJ", "airline_name": "Jin Air", "color_code": "#FFD700"},
        {"airline_code": "ZE", "airline_name": "Eastar Jet", "color_code": "#00A651"},
        {"airline_code": "BX", "airline_name": "Air Busan", "color_code": "#FF6B35"},
        {"airline_code": "RS", "airline_name": "Air Seoul", "color_code": "#003366"},
    ]

    created = []
    for airline_data in default_airlines:
        existing = db.query(Airline).filter(
            Airline.airline_code == airline_data["airline_code"]
        ).first()
        if not existing:
            db_airline = Airline(**airline_data)
            db.add(db_airline)
            created.append(db_airline)

    db.commit()
    for airline in created:
        db.refresh(airline)

    return created
