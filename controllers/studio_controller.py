from typing import List
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.anime_model import Anime
from models.studio_model import Studio
from schemas.anime_validator import AnimeResponse
from schemas.studio_validator import StudioResponse, StudioValidator, StudioUpdate

from utils.uuid_conv import binary_to_uuid, uuid_to_binary


def add_new_studio(studio_data:StudioValidator, db:Session) -> StudioResponse:
    try:
        new_studio = Studio(
            uuid=uuid4().bytes,
            name=studio_data.name
        )

        db.add(new_studio)
        db.commit()
        db.refresh(new_studio)

        return StudioResponse.model_validate(new_studio)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="bad request"
        )


def delete_studio(studio_data:StudioResponse, db:Session):
    binary_uuid = uuid_to_binary(studio_data.uuid)

    studio = db.execute(
        select(Studio).where(
            or_(Studio.name == studio_data.name,
                Studio.uuid == binary_uuid)
        )
    ).scalar_one_or_none()

    if studio is None:
        raise HTTPException(
            status_code=404,
            detail=f"Studio '{studio_data.name}' not found !"
        )

    try:
        db.delete(studio)
        db.commit()
        return {"detail": f"Studio '{studio_data.name}' deleted successfully."}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not delete studio due to existing anime entries associated with it"
        )


def get_studio(studio_data: StudioResponse, db:Session) -> StudioResponse:
    binary_uuid = uuid_to_binary(studio_data.uuid)

    studio = db.execute(
        select(Studio).where(
            or_(Studio.name == studio_data.name,
                Studio.uuid == binary_uuid)
        )
    ).scalar_one_or_none()

    if studio is None:
        raise HTTPException(
            status_code=404,
            detail=f"Studio '{studio_data.name}' is not found !"
        )

    return StudioResponse.model_validate(studio)


def get_all_studios(db:Session) -> List[StudioResponse]:
    studios = db.execute(
        select(Studio).order_by(Studio.name)
    ).scalars().all()

    return [StudioResponse.model_validate(s) for s in studios]


def all_anime_by_studio(studio_data:StudioValidator, db:Session) -> List[AnimeResponse]:
    binary_uuid = uuid_to_binary(studio_data.uuid)

    studio = db.execute(
        select(Studio).where(
            or_(Studio.name == studio_data.name,
                Studio.uuid == binary_uuid)
        )
    ).scalar_one_or_none()

    if studio is None:
        raise HTTPException(
            status_code=404,
            detail=f"Studio '{studio_data.name}' is not found !"
        )

    anime_by_studio = db.execute(
        select(Anime).where(Anime.studio == studio.uuid).order_by(Anime.name)
    ).scalars().all()

    return [AnimeResponse.model_validate(a) for a in anime_by_studio]


def update_studio(studio_id_data: StudioResponse, studio_data: StudioUpdate, db:Session) -> StudioResponse:
    binary_uuid = uuid_to_binary(studio_id_data.uuid)

    studio = db.execute(
        select(Studio).where(
            or_(Studio.name == studio_id_data.name,
                Studio.uuid == binary_uuid)
        )
    ).scalar_one_or_none()

    if studio is None:
        raise HTTPException(
            status_code=404,
            detail=f"Studio '{studio_id_data.name}' is not found !"
        )

    update_data = studio_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        studio.name = update_data["name"]

    try:
        db.commit()
        db.refresh(studio)
        return StudioResponse.model_validate(studio)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Bad request! Likely a duplicate studio name."
        )

