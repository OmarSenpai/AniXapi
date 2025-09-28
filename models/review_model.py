from sqlalchemy import Column, String, BINARY, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"
    uuid = Column(BINARY, primary_key=True, nullable=False, unique=True)
    anime = Column(ForeignKey("anime.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user = Column(ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    body = Column(String)
    published = Column(TIMESTAMP)

    __table_args__ = (
        PrimaryKeyConstraint ("user","anime")
    )

