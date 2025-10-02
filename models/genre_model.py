from sqlalchemy import Column, Integer, String, BINARY, Enum, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Genre(Base):
    __tablename__ = "anime"
    uuid = Column(BINARY, primary_key = True)
    name = Column(String)

