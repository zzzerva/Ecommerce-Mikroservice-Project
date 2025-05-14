from fastapi import FastAPI
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import auth, user, address, contact

# Create database tables
"""Base.metadata.create_all(bind=engine)"""

app = FastAPI(title="User Service")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

"""app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)"""

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(user.router, prefix=settings.API_V1_STR)
app.include_router(address.router, prefix=settings.API_V1_STR)
app.include_router(contact.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "Welcome to User Service API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 