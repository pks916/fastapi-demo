from pydantic import BaseModel, EmailStr

from datetime import datetime


#pydantic models
class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass

class PostRespose(PostBase):
    id:int
    created_at:datetime

    class Config():
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr

    class Config():
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str