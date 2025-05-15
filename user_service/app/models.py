from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, JSON
from sqlalchemy.orm import relationship
import enum
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class CategoryType(str, enum.Enum):
    HOME = "home"
    WORK = "work"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="User")
    is_active = Column(Boolean, default=True)
    full_name = Column(String)
    force_password_change = Column(Boolean, default=False)

    addresses = relationship("Address", back_populates="user")
    contacts = relationship("Contact", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)
    
    user = relationship("User", back_populates="addresses")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    phone_type = Column(String)
    phone_number = Column(String)
    
    user = relationship("User", back_populates="contacts")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = Column(JSON, default=list) 