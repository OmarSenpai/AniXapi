from sqlalchemy import Column, String, BINARY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Studio(Base):
    __tablename__ = "studios"
    uuid = Column(BINARY, primary_key = True, nullable=False)
    name = Column(String, unique=True, nullable=False)
