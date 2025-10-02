from fastapi import APIRouter, FastAPI, Depends
from controllers.anime_controller import *
from schemas.anime_validator import *
from utils.db_connection import *
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Anime"],
    prefix="/anime"
)

@router.post("/", response_model=AnimeResponse)
def new_anime(
        anime_data: NewAnime,
        db: Session = Depends(db_conn)
):
    return add_new_anime(anime_data ,db)


@router.get("/")
def all_anime(
        db:Session = Depends(db_conn)
):
    return get_all_anime(db)

