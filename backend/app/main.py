"""
BetaShift - Carousel Assignment Automation System
FastAPI Main Application
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models import Airline, Carousel, Flight, Assignment  # noqa: F401


# =============================================================================
# Lifespan (App startup/shutdown events)
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application lifecycle.
    - Startup: DB connection, initial data loading, etc.
    - Shutdown: DB disconnect, resource cleanup, etc.
    """
    # === Startup ===
    print("BetaShift server starting...")

    # Create all tables if they don't exist
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables ready!")

    yield  # App runs at this point

    # === Shutdown ===
    print("BetaShift server shutting down...")


# =============================================================================
# FastAPI App Creation
# =============================================================================

app = FastAPI(
    title="BetaShift",
    description="Airport Arrival Baggage Carousel Assignment Automation System",
    version="0.1.0",
    lifespan=lifespan,
)


# =============================================================================
# CORS Settings (Allow frontend communication)
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # React dev server
        "http://localhost:5173",     # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],             # Allow all HTTP methods
    allow_headers=["*"],             # Allow all headers
)


# =============================================================================
# Router Registration
# =============================================================================

from app.routers import airlines, carousels, flights, assignments

app.include_router(airlines.router, prefix="/api/airlines", tags=["airlines"])
app.include_router(carousels.router, prefix="/api/carousels", tags=["carousels"])
app.include_router(flights.router, prefix="/api/flights", tags=["flights"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["assignments"])


# =============================================================================
# Default Endpoints (Health Check)
# =============================================================================

@app.get("/")
async def root():
    """Root path - API status check"""
    return {
        "service": "BetaShift",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint - Server status check"""
    return {"status": "healthy"}


# =============================================================================
# Database Test Endpoint (TEMPORARY - Remove after verification)
# =============================================================================

@app.get("/db-test")
async def db_test():
    """
    Database connection test - TEMPORARY
    Remove this endpoint after confirming DB connection works.
    """
    from app.database import engine

    try:
        with engine.connect() as conn:
            return {"database": "connected"}
    except Exception as e:
        return {"database": "failed", "error": str(e)}
