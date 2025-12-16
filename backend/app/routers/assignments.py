"""
Assignments API Router
CRUD operations for carousel assignment management
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Assignment, Flight, Carousel
from app.schemas import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
    AssignmentWithDetailsResponse,
)

router = APIRouter()


@router.get("/", response_model=list[AssignmentWithDetailsResponse])
def get_assignments(
    date: str | None = Query(None, description="Filter by date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get all assignments.
    Optionally filter by date (YYYY-MM-DD).
    """
    query = db.query(Assignment)

    if date:
        try:
            filter_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(
                Assignment.start_time >= datetime.combine(filter_date, datetime.min.time()),
                Assignment.start_time < datetime.combine(filter_date, datetime.max.time())
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    assignments = query.all()
    return assignments


@router.get("/{assignment_id}", response_model=AssignmentWithDetailsResponse)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Get a specific assignment by ID."""
    assignment = db.query(Assignment).filter(
        Assignment.assignment_id == assignment_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.post("/", response_model=AssignmentResponse, status_code=201)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """Create a new assignment."""
    # Check if flight exists
    flight = db.query(Flight).filter(Flight.flight_id == assignment.flight_id).first()
    if not flight:
        raise HTTPException(status_code=400, detail="Flight not found")

    # Check if carousel exists
    carousel = db.query(Carousel).filter(
        Carousel.carousel_id == assignment.carousel_id
    ).first()
    if not carousel:
        raise HTTPException(status_code=400, detail="Carousel not found")

    # Check if carousel is active
    if not carousel.is_active:
        raise HTTPException(status_code=400, detail="Carousel is not active")

    db_assignment = Assignment(**assignment.model_dump())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.put("/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(
    assignment_id: int,
    assignment: AssignmentUpdate,
    db: Session = Depends(get_db)
):
    """Update an assignment (for manual adjustments)."""
    db_assignment = db.query(Assignment).filter(
        Assignment.assignment_id == assignment_id
    ).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Only update fields that were provided
    update_data = assignment.model_dump(exclude_unset=True)

    # If carousel is being changed, verify it exists and is active
    if "carousel_id" in update_data:
        carousel = db.query(Carousel).filter(
            Carousel.carousel_id == update_data["carousel_id"]
        ).first()
        if not carousel:
            raise HTTPException(status_code=400, detail="Carousel not found")
        if not carousel.is_active:
            raise HTTPException(status_code=400, detail="Carousel is not active")

    for field, value in update_data.items():
        setattr(db_assignment, field, value)

    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.delete("/{assignment_id}", status_code=204)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Delete an assignment."""
    assignment = db.query(Assignment).filter(
        Assignment.assignment_id == assignment_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(assignment)
    db.commit()
    return None
