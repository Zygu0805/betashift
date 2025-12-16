"""
Carousels API Router
CRUD operations for carousel management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Carousel
from app.schemas import CarouselCreate, CarouselUpdate, CarouselResponse

router = APIRouter()


@router.get("/", response_model=list[CarouselResponse])
def get_carousels(db: Session = Depends(get_db)):
    """Get all carousels."""
    carousels = db.query(Carousel).all()
    return carousels


@router.get("/{carousel_id}", response_model=CarouselResponse)
def get_carousel(carousel_id: str, db: Session = Depends(get_db)):
    """Get a specific carousel by ID."""
    carousel = db.query(Carousel).filter(Carousel.carousel_id == carousel_id).first()
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")
    return carousel


@router.post("/", response_model=CarouselResponse, status_code=201)
def create_carousel(carousel: CarouselCreate, db: Session = Depends(get_db)):
    """Create a new carousel."""
    existing = db.query(Carousel).filter(
        Carousel.carousel_id == carousel.carousel_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Carousel already exists")

    db_carousel = Carousel(**carousel.model_dump())
    db.add(db_carousel)
    db.commit()
    db.refresh(db_carousel)
    return db_carousel


@router.patch("/{carousel_id}", response_model=CarouselResponse)
def update_carousel(
    carousel_id: str,
    carousel: CarouselUpdate,
    db: Session = Depends(get_db)
):
    """Update a carousel (partial update)."""
    db_carousel = db.query(Carousel).filter(Carousel.carousel_id == carousel_id).first()
    if not db_carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    # Only update fields that were provided
    update_data = carousel.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_carousel, field, value)

    db.commit()
    db.refresh(db_carousel)
    return db_carousel


@router.post("/init", response_model=list[CarouselResponse], status_code=201)
def init_carousels(db: Session = Depends(get_db)):
    """
    Initialize carousels C1 ~ C24.
    Call this once to set up initial data.
    """
    created = []
    for i in range(1, 25):  # C1 ~ C24
        carousel_id = f"C{i}"
        existing = db.query(Carousel).filter(Carousel.carousel_id == carousel_id).first()
        if not existing:
            # T1: C1~C12, T2: C13~C24
            terminal = "T1" if i <= 12 else "T2"
            db_carousel = Carousel(
                carousel_id=carousel_id,
                terminal=terminal,
                capacity=100,
                is_active=True
            )
            db.add(db_carousel)
            created.append(db_carousel)

    db.commit()
    for carousel in created:
        db.refresh(carousel)

    return created
