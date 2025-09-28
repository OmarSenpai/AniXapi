from fastapi import APIRouter, FastAPI, Depends
from controllers.auth_controller import *
from schemas.auth_validator import *
from utils.db_connection import *

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)

@router.post("/register")
async def register_new_user(user: UserCreate, db: Session = Depends(db_conn)):
    return register_user(user, db)


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(db_conn)):
    return user_login(user, db)

