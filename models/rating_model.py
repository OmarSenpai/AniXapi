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

@event.listens_for(Rating, 'before_insert')
@event.listens_for(Rating, 'before_update')
def check_rating(mapper, connection, target):
    rating = target.value
    if rating < 0 or rating > 5:
        raise ValueError("Rating must be not less than 0 and not greater than 5")
    return rating
