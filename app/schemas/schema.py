
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from typing import Optional

class createPost(BaseModel):
    title: str
    description: str =  Field(min_length=3)
    is_published: bool = True

class resposePost(createPost):
    created_at: datetime
    owner_id: int




class returnPost(createPost):
    created_at: datetime
    owner_id: int
    owner: createUser


class createUser(BaseModel):
    email: EmailStr
    password: str
    name: str
    job: str | None =None

class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
class loginUser(BaseModel):
    email: EmailStr
    passsword: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None
    # created_at: datetime

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]