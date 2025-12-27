from sqlalchemy.orm import Session
from app.models.users import User,UserRole
from app.schemas.user import UserCreate
from app.utils.security import hash_password,verify_password
from typing import Optional

def create_user(db:Session, user_in:UserCreate)->User:
    user = User(
        name = user_in.name,
        phone_number = user_in.phone_number,
        email = user_in.email.lower(),
        password_hash = hash_password(user_in.password),
        role = UserRole.CUSTOMER
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db:Session, email:str):
    return db.query(User).filter(User.email==email).first()

def authenticate_user(db:Session, email:str, password:str)->Optional[User]:
    user = get_user(db,email)

    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None

    return user


