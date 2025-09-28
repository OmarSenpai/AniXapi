import sqlalchemy
from sqlalchemy import func
from sqlalchemy import Column, Integer, String, BINARY, DateTime, Boolean, Enum, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from argon2 import PasswordHasher
from schemas.auth_validator import *

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    uuid = Column(BINARY, primary_key = True)
    username = Column(String, unique=True, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    role = Column(Enum("user","admin"), default="user")

