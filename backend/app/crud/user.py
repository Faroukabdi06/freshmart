from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.models.users import User,UserRole
from app.schemas.user import UserCreate
from app.utils.security import hash_password,verify_password



def create_user(db:Session, user_in:UserCreate)->User:
    user = User(
        name = user_in.name,
        phone_number = user_in.phone_number,
        email = user_in.email.lower(),
        password_hash = hash_password(user_in.password),
        role = user_in.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db:Session, email:str):
    return db.query(User).filter(User.email==email.lower()).first()

def get_user_id(db:Session, user_id:UUID):
    return db.query(User).filter(User.id == user_id).first()

def authenticate_user(db:Session, email:str, password:str)->Optional[User]:
    user = get_user(db,email)

    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None

    return user


