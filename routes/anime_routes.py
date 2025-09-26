from fastapi import APIRouter, FastAPI, Depends
from controllers.auth_controller import *
from schemas.auth_validator import *
from utils.db_connection import *

router = APIRouter(
    tags=["Anime"],
    prefix="/anime"
)

@router.post("/register")
def register_new_user(user: user_create, db: Session = Depends(db_conn)):
    return register_user(user, db)

@router.post("/login")
def login_user(user: user_login, db: Session = Depends(db_conn)):
    return login_user


