from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine
from app.core.models import Base
from typing import Dict

# SQLAlchemy 2.x style for table creation
with engine.begin() as conn:
    Base.metadata.create_all(bind=conn)

app = FastAPI(
    title="Product Service",
    description="Product management microservice for e-commerce system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to Product Service API"} 