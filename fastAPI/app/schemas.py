from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime
class Post(BaseModel):
    # id:int
    title: str
    content: str
    publish: bool = True

class CreatePost(BaseModel): 
    title: str
    content: str
    publish: bool = True

class UpdatePost(BaseModel):
    publish: bool

class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str 


class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str]