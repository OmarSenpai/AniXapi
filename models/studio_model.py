import sqlalchemy
from sqlalchemy import Column, Integer, String, BINARY, DateTime, Boolean, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy import event

Base = declarative_base()

class Studio(Base):
    __tablename__ = "studios"
    uuid = Column(BINARY, primary_key = True)
    name = Column(String)


