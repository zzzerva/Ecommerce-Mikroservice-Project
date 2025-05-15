from fastapi import FastAPI
from .database import engine
from . import models

print("Creating tables...")
models.Base.metadata.create_all(bind=engine)
print("Tables created.")

app = FastAPI(title="User Service")

from app.routers import auth, users, roles

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)
