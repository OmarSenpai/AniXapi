import sqlalchemy
from sqlalchemy import Column, Integer, String, BINARY, DateTime, Boolean, Enum, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import event

Base = declarative_base()

class Anime(Base):
    __tablename__ = "anime"
    uuid = Column(BINARY, primary_key = True)
    name = Column(String)
    jp_name = Column(String)
    episodes = Column(Integer)
    format = Column(Enum("TV","movie"))
    start_date = Column(Date)
    end_date = Column(Date)
    studio = Column(ForeignKey("studios.uuid", ondelete="CASCADE"), nullable=False)

