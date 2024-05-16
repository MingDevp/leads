from fastapi import File
from sqlmodel import Field, SQLModel
from typing import Annotated


# Shared properties
class LeadBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str


# Database model, database table inferred from class name
class Lead(LeadBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    resume: Annotated[bytes, File()]
    state: str


# Properties to return via API, id is always required
class LeadPublic(LeadBase):
    id: int


class LeadsPublic(SQLModel):
    data: list[Lead]
    count: int


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Shared properties
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
