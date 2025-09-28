from sqlalchemy import Column, Integer, String, BINARY, Enum, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Anime(Base):
    __tablename__ = "anime"
    uuid = Column(BINARY, primary_key = True)
    name = Column(String, unique=True, nullable=False)
    jp_name = Column(String, nullable=False)
    episodes = Column(Integer)
    format = Column(Enum("TV","movie"))
    start_date = Column(Date)
    end_date = Column(Date)
    studio = Column(ForeignKey("studios.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

