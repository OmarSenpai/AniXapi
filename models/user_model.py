import sqlalchemy
from sqlalchemy import Column, Integer, String, BINARY, DateTime, Boolean, Enum, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from argon2 import PasswordHasher

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    uuid = Column(BINARY, primary_key = True)
    username = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    role = Column(Enum("user","admin"))

# hash password before saving user data
@event.listens_for(User, 'before_insert')
def hash_password(mapper, connection, target):
    ph = PasswordHasher()
    target.password = ph.hash(target.password)
    return target.password
