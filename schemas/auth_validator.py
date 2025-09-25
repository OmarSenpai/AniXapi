import pydantic
from pydantic import BaseModel, EmailStr

class user_create(BaseModel):
    username: str
    email: EmailStr
    password: str


class user_login(BaseModel):
    username: str
    password: str


class forgot_password(BaseModel):
    token: str
    email: EmailStr


class reset_password(BaseModel):
    email: EmailStr

