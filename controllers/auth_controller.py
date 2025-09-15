from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import user_model
from schemas.auth_validator import *


def register_user(user:user_create, db:Session):
    try:
        new_user = user_model.User(
            uuid=uuid4().bytes,
            email=user.email,
            password=user.password,
            username=user.username,
            role="user"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Bad request"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error :{e}"
        )


def login_user(user_credentials:user_login, db:Session):
    try:


def generate_token():
    return

