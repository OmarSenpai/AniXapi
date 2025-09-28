import argon2, jwt, os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import *
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

load_dotenv()
ph = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def verify_password(plain_password, hashed_password) -> tuple[bool, str | None]:
    try:
        match = ph.verify(hashed_password, plain_password)

        if match and ph.check_needs_rehash(hashed_password):
            return True, ph.hash(plain_password)

        return True, None

    except (InvalidHashError,VerifyMismatchError):
        return False, None


def create_access_token(data:dict, expire_delta:timedelta | None = None) -> str:
    wt_load = data.copy()
    if "sub" not in wt_load:
        raise ValueError("Token payload must contain a 'sub' claim")

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    wt_load.update({"exp":expire})

    try:
        encoded_jwt = jwt.encode(wt_load,SECRET_KEY,algorithm=[ALGORITHM])
        return encoded_jwt

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Could not create access token"
        )


def verify_jwt(token:str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("sub")

        if user_id is None:
            return None

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate":"Bearer"}
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )

