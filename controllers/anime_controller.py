from typing import List
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import Session, select, or_
from sqlalchemy.exc import IntegrityError
from models.anime_model import Anime
from models.studio_model import Studio
from schemas.anime_validator import AnimeResponse, NewAnime, AnimeUpdate
from utils.uuid_conv import uuid_to_binary


def add_new_anime(anime_data:NewAnime, db:Session) -> AnimeResponse:
    try:
        studio_binary_uuid = uuid_to_binary(anime_data.studio_uuid)

        studio = db.execute(
            select(Studio).where(
                Studio.uuid == studio_binary_uuid
            )
        ).scalar_one_or_none()

        if not studio:
            raise HTTPException(
                status_code=404,
                detail="Studio does not exist"
            )

        new_anime = Anime(
            uuid=uuid4().bytes,
            name=anime_data.name,
            jp_name=anime_data.jp_name,
            episodes=anime_data.episodes,
            format=anime_data.format,
            start_date=anime_data.start_date,
            end_date=anime_data.end_date,
            studio=studio_binary_uuid
        )

        db.add(new_anime)
        db.commit()
        db.refresh(new_anime)

        return AnimeResponse.model_validate(new_anime)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Bad request !"
        )


def get_all_anime(db:Session) -> List[AnimeResponse]:
    anime = db.execute(
        select(Anime).order_by(Anime.name)
    ).scalars().all()

    return [AnimeResponse.model_validate(a) for a in anime]


def get_anime(anime_data: AnimeResponse, db:Session) -> AnimeResponse:
    binary_uuid = uuid_to_binary(anime_data.uuid)

    anime = db.execute(
        select(Anime).where(
            or_(Anime.name == anime_data.name,
                Anime.uuid == binary_uuid)
        )
    ).scalar_one_or_none()

    if anime is None:
        raise HTTPException(
            status_code=404,
            detail=f"Anime '{anime_data.name}' not found"
        )

    return AnimeResponse.model_validate(anime)


def delete_anime(anime_data:AnimeResponse, db:Session):
    binary_uuid = uuid_to_binary(anime_data.uuid)

    anime = db.execute(
        select(Anime).where(
            or_(Anime.name == anime_data.name,
            Anime.uuid == binary_uuid)
        )
    ).scalar_one_or_none()

    if anime is None:
        raise HTTPException(
            status_code=404,
            detail=f"Anime '{anime_data.name}' not found !"
        )

    try:
        db.delete(anime)
        db.commit()
        return {"detail": f"Anime '{anime_data.name}' deleted successfully."}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not delete the requested anime"
        )


def update_anime(anime_id_data: AnimeResponse, anime_data: AnimeUpdate, db: Session) -> AnimeResponse:
    binary_uuid = uuid_to_binary(anime_id_data.uuid) if anime_id_data.uuid else None

    anime = db.execute(
        select(Anime).where(
            or_(Anime.name == anime_id_data.name,
                Anime.uuid == binary_uuid)
        )
    ).scalar_one_or_none()

    if anime is None:
        raise HTTPException(
            status_code=404,
            detail=f"Anime '{anime_id_data.name}' not found"
        )

    update_data = anime_data.model_dump(exclude_unset=True)

    # Handle Studio Update (by UUID or Name)
    new_studio_binary_uuid = None

    if "studio_uuid" in update_data or "studio_name" in update_data:
        studio_lookup_uuid = update_data.pop("studio_uuid", None)
        studio_lookup_name = update_data.pop("studio_name", None)

        if studio_lookup_uuid:
            # Lookup by UUID provided in the update payload
            studio_binary_uuid = uuid_to_binary(studio_lookup_uuid)

            studio = db.execute(
                select(Studio).where(Studio.uuid == studio_binary_uuid)
            ).scalar_one_or_none()

        elif studio_lookup_name:
            # Lookup by Name provided in the update payload
            studio = db.execute(
                select(Studio).where(Studio.name == studio_lookup_name)
            ).scalar_one_or_none()
        else:
            # Should not happen if at least one of the keys was present in update_data
            studio = None

        if not studio:
            raise HTTPException(
                status_code=404,
                detail="New Studio specified (by UUID or Name) does not exist"
            )

        new_studio_binary_uuid = studio.uuid

    # Apply other fields first
    for key, value in update_data.items():
        setattr(anime, key, value)

    # Apply the new studio UUID if it was found
    if new_studio_binary_uuid:
        anime.studio = new_studio_binary_uuid

    try:
        if (getattr(anime, 'start_date', None) and getattr(anime, 'end_date', None) and
                anime.start_date > anime.end_date):
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Start date cannot come after end date!"
            )

        db.commit()
        db.refresh(anime)
        return AnimeResponse.model_validate(anime)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Bad request! Likely a duplicate anime name or other constraint violation."
        )


