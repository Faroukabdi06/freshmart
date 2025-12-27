from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime,timedelta

from app.crud.user import create_user,get_user,authenticate_user
from app.schemas.user import UserCreate,UserResponse,UserLogin
from app.cores.database import get_db
from app.cores.config import Config
from app.utils.security import create_access_token

router = APIRouter(tags=["auth"])

@router.post("/signup", response_model=UserResponse)
def signup(user_in:UserCreate, db:Session=Depends(get_db)):

    check_user = get_user(db,user_in.email)

    if check_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "user already exists"
        )
    user = create_user(db,user_in)
    return user

@router.post("/login")
def login(user_in:UserLogin, db:Session=Depends(get_db)):
    user = authenticate_user(db,user_in.email.lower(),user_in.password)

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub":str(user.id)},
        expires = access_token_expires
    )
    return { "access_token":access_token, "token_type":"bearer"}