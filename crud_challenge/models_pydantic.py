from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class UserRequest(BaseModel):
    username: str = Field(
        min_length=4,
    )
    email: EmailStr
    first_name: str = Field(min_length=4, max_length=10)
    last_name: str = Field(min_length=4, max_length=10)
    role: Role = Role.user
    active: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "fede1234",
                "email": "fede1234@gmail.com",
                "first_name": "Federico",
                "last_name": "Test",
                "role": "admin",
                "active": True,
            }
        }
    }


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=4)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(default=None, min_length=4, max_length=10)
    last_name: Optional[str] = Field(default=None, min_length=4, max_length=10)
    role: Optional[Role] = None
    active: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "fede1234",
                "email": "fede1234@gmail.com",
                "first_name": "Federico",
                "last_name": "Test",
                "role": "admin",
                "active": True,
            }
        }
    }


class UserCreate(UserRequest):
    id: Optional[int] = Field(default=None, description=" ID is not needed on create")
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, description="By default it takes datetime.now()"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now, description="Updated when modified"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "fede1234",
                "email": "fede1234@gmail.com",
                "first_name": "Federico",
                "last_name": "Test",
                "role": "admin",
                "active": True,
            }
        }
    }
