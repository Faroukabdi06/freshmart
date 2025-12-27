from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta
from typing import Optional

from app.cores.config import Config

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)


def create_access_token(data: dict, expires: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt