from pydantic import BaseModel, EmailStr, constr, field_validator, ConfigDict
from typing import Optional, List
from .models import UserRole, CategoryType

class ErrorMessages:
    INVALID_CREDENTIALS = "Invalid credentials"
    USER_NOT_FOUND = "User not found"
    INSUFFICIENT_PERMISSIONS = "Insufficient permissions"
    USERNAME_EXISTS = "Username already exists"
    EMAIL_EXISTS = "Email already exists"
    INVALID_PASSWORD = "Password requirements not met"
    INVALID_ROLE = "Invalid role"

class AddressBase(BaseModel):
    type: str
    street: str
    city: str
    state: str
    country: str
    postal_code: str

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class ContactBase(BaseModel):
    phone_type: str
    phone_number: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    username: str
    email: EmailStr

    @field_validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must contain only letters and numbers')
        return v

class UserCreate(UserBase):
    password: constr(min_length=8)
    role: str = "User"

    @field_validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

    @field_validator('role')
    def validate_role(cls, v):
        if v not in ["User", "Admin"]:
            raise ValueError(ErrorMessages.INVALID_ROLE)
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None
    role: Optional[str] = None

class User(UserBase):
    id: int
    role: str
    is_active: bool = True
    full_name: Optional[str] = None
    addresses: List[Address] = []
    contacts: List[Contact] = []

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None

class RoleBase(BaseModel):
    name: str
    permissions: List[str]

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Validation schemas
class PasswordChange(BaseModel):
    old_password: str
    new_password: constr(min_length=8)

class PasswordReset(BaseModel):
    new_password: constr(min_length=8)

class UserStatus(BaseModel):
    is_active: bool

class AddressCreate(BaseModel):
    type: str
    street: str
    city: str
    state: str
    country: str
    postal_code: str

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class ContactCreate(BaseModel):
    phone_type: str
    phone_number: str

class RoleCreate(BaseModel):
    name: str
    permissions: List[str]

class RoleUpdate(BaseModel):
    permissions: List[str]

class PermissionAdd(BaseModel):
    permission: str