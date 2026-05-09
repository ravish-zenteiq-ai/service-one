from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class createPost(BaseModel):
    title: str
    description: str =  Field(min_length=3)
    is_published: bool = True

class returnPost(createPost):
    created_at: datetime


class createUser(BaseModel):
    email: EmailStr
    password: str
    name: str
    job: str | None =None

class loginUser(BaseModel):
    email: EmailStr
    passsword: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None
    # created_at: datetime