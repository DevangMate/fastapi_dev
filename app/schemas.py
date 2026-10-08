from pydantic import BaseModel,ConfigDict,EmailStr,Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    model_config=ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Postbase(BaseModel):
    title:str
    content:str
    published:bool=True
    

class PostCreate(Postbase):
    pass


class Post(Postbase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    
    model_config = ConfigDict(from_attributes=True)

class Postout(BaseModel):
    Post:Post
    votes:int
    model_config = ConfigDict(from_attributes=True)
    

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id:int
    dir:int=Field(ge=0, le=1)