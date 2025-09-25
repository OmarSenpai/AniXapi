import sqlalchemy
from sqlalchemy import Column, Integer, String, BINARY, DateTime, Boolean, Enum, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from datetime import date
from typing import cast, Optional

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

@event.listens_for(Anime, 'before_insert')
@event.listens_for(Anime, 'before_update')
def check_anime_date(mapper, connection, target):
    sdt = target.start_date
    edt = target.end_date

    if sdt > edt:
        raise ValueError("start date can't come after end date !")
