from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt, hashlib, os
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["sha256_crypt"])

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def return_password(password):
    pwd_context.hash(password)

def create_access_token(data:dict):
    wt_load = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    wt_load.update({"exp":expire})
    encoded_jwt = jwt.encode(wt_load,SECRET_KEY,ALGORITHM)
    return wt_load

def verify_jwt(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.exceptions.InvalidTokenError:
        return None
