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
    id: int = Field(default=None, description=" ID is not needed on create")
    created_at: datetime = Field(
        default_factory=datetime.now, description="By default it takes datetime.now()"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Updated when modified"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "fede1234",
                "email": "fede1234@gmail.com",
                "first_name": "Federico",
                "last_name": "Test",
                "role": "admin",
                "active": True,
                "created_at": "2025-04-19T23:14:49.155681",
                "updated_at": "2025-04-19T20:31:16.938253",
            }
        }
    }
