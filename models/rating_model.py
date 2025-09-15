import sqlalchemy
from sqlalchemy import Column, Integer, String, BINARY, DateTime, Boolean, Enum, TIMESTAMP, ForeignKey, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from argon2 import PasswordHasher

Base = declarative_base()

class Rating(Base):
    __tablename__ = "ratings"
    uuid = Column(BINARY, primary_key = True)
    anime = Column(ForeignKey("anime.uuid", ondelete="CASCADE"), nullable=False)
    user = Column(ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
    value = Column(Float)