from fastapi import APIRouter, FastAPI, Depends
from controllers.rating_controller import *
from schemas.rating_validator import *
from utils.db_connection import *

router = APIRouter(
    tags=["Rating"],
    prefix="/rating"
)

@router.post("/register")
def rate_anime(user: user_create, db: Session = Depends(db_conn)):
    return rate_anime(user, db)


