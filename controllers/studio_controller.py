from models.studio_model import *
from models.anime_model import *
from fastapi import HTTPException
from schemas import studio_validator
from sqlalchemy import select, delete, insert, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from utils.db_connection import *

def add_new_studio(studio:studio_validator, db:Session):
    try:
        new_studio = Studio(
            uuid=uuid4().bytes,
            name=studio.name
        )

        db.add(new_studio)
        db.commit()
        db.refresh(new_studio)
        return new_studio

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="bad request"
        )


def delete_studio(studio_name:studio_validator, db:Session):
    studio = db.execute(select(Studio).where(Studio.name == studio_name.name)).scalar_one_or_none()

    if studio is None:
        raise HTTPException(
            status_code=400,
            detail=f"Studio '{studio_name}' not found !"
        )

    try:
        db.delete(studio)
        db.commit()
        return {"detail": f"Studio '{studio_name}' deleted successfully."}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not delete studio !"
        )


def get_studios(db:Session):
    studios = db.execute(select(Studio).order_by(Studio.name)).scalars().all()
    return studios


def all_anime_by_studio(db:Session):
    anime_by_studio = db.execute(select(Anime).where(Studio.name)).scalars().all()
    return anime_by_studio