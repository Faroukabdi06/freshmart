from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime,timedelta
from typing import Optional
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import UUID

from app.cores.config import Config
from app.cores.database import get_db
from app.schemas.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
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


def get_current_user(
    token:str= Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    from app.crud.user import get_user_id
    credentials_error = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credantials",
        headers = {"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms = [Config.ALGORITHM]
        )
        user_id :str = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user = get_user_id(db, UUID(user_id))
    if user is None:
        raise credentials_error

    return user


