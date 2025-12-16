"""
Flights API Router
CRUD operations for flight management
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Flight, Airline
from app.schemas import FlightCreate, FlightResponse, FlightWithAirlineResponse

router = APIRouter()


@router.get("/", response_model=list[FlightWithAirlineResponse])
def get_flights(
    date: str | None = Query(None, description="Filter by date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get all flights.
    Optionally filter by date (YYYY-MM-DD).
    """
    query = db.query(Flight)

    if date:
        # Parse date and filter by scheduled_time
        try:
            filter_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(
                Flight.scheduled_time >= datetime.combine(filter_date, datetime.min.time()),
                Flight.scheduled_time < datetime.combine(filter_date, datetime.max.time())
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    flights = query.all()
    return flights


@router.get("/{flight_id}", response_model=FlightWithAirlineResponse)
def get_flight(flight_id: str, db: Session = Depends(get_db)):
    """Get a specific flight by ID."""
    flight = db.query(Flight).filter(Flight.flight_id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@router.post("/", response_model=FlightResponse, status_code=201)
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    """Create a new flight."""
    # Check if flight already exists
    existing = db.query(Flight).filter(Flight.flight_id == flight.flight_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Flight already exists")

    # Check if airline exists
    airline = db.query(Airline).filter(Airline.airline_code == flight.airline).first()
    if not airline:
        raise HTTPException(status_code=400, detail=f"Airline '{flight.airline}' not found")

    db_flight = Flight(**flight.model_dump())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


@router.post("/upload", response_model=list[FlightResponse], status_code=201)
def upload_flights(flights: list[FlightCreate], db: Session = Depends(get_db)):
    """
    Bulk upload flights from JSON.
    Skips flights that already exist.
    """
    created = []
    for flight_data in flights:
        existing = db.query(Flight).filter(
            Flight.flight_id == flight_data.flight_id
        ).first()
        if not existing:
            db_flight = Flight(**flight_data.model_dump())
            db.add(db_flight)
            created.append(db_flight)

    db.commit()
    for flight in created:
        db.refresh(flight)

    return created


@router.delete("/{flight_id}", status_code=204)
def delete_flight(flight_id: str, db: Session = Depends(get_db)):
    """Delete a flight."""
    flight = db.query(Flight).filter(Flight.flight_id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    db.delete(flight)
    db.commit()
    return None
