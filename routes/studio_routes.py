from typing import List
from fastapi import APIRouter, FastAPI, Depends
from controllers.studio_controller import *
from schemas.studio_validator import *
from utils.db_connection import *
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Studio"],
    prefix="/studios"
)


@router.post("/", response_model=StudioResponse)
def create_studio(
        studio_data: StudioValidator,
        db: Session = Depends(db_conn)
):
    return add_new_studio(studio_data, db)


@router.delete("/")
def remove_studio(
        studio_data: StudioValidator,
        db: Session = Depends(db_conn)
):
    return delete_studio(studio_data ,db)


@router.get("/", response_model=List[StudioResponse])
def read_all_studios(
        db: Session = Depends(db_conn)
):
    return get_all_studios(db)


@router.get("/")
def all_studio_anime(
        studio_data: StudioValidator,
        db: Session = Depends(db_conn)
):
    return all_anime_by_studio(studio_data ,db)

