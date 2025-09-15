import sqlalchemy
from sqlalchemy import Column, Integer, String, BINARY, DateTime, Boolean, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from argon2 import PasswordHasher

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"
    uuid = Column(BINARY, primary_key = True)
    anime = Column(ForeignKey("anime.uuid", ondelete="CASCADE"), nullable=False)
    user = Column(ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
    body = Column(String)
    published = Column(TIMESTAMP)
