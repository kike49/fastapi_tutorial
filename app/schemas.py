from datetime import datetime
from pydantic import BaseModel, EmailStr


# User schemas
class UserOut(BaseModel):
    email: EmailStr
    id: int
    registered_on: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Posts schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str


# Votes schemas
class Vote(BaseModel):
    post_id: int
    dir: int # Will be 0 or 1 for like or dislike