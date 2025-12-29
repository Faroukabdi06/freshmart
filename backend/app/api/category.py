from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.user import UserResponse
from app.schemas.category import CategoryResponse,CategoryCreate,CategoryUpdate
from app.cores.database import get_db
from app.crud.category import (
    create_category, get_all_categories, get_category,
    update_category, disable_category,
    get_category_by_name, activate, get_all_categories_admin
)
from app.utils.security import get_current_user

router = APIRouter(tags=["category"])

@router.post("/categories",response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
def create(
    category_in:CategoryCreate,
    db:Session=Depends(get_db),
    current_user:UserResponse=Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You don't have authorization"
            )

    existing = get_category_by_name(db, category_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists"
        )
    return create_category(db,category_in)


@router.get("/categories", response_model=List[CategoryResponse],status_code=status.HTTP_200_OK)
def all_categories(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
    if current_user.role == "customer":
        return get_all_categories(db)
    return get_all_categories_admin(db)

@router.get("/categories/{id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def one_category(id:UUID,current_user:UserResponse=Depends(get_current_user),db:Session=Depends(get_db)):
    category = get_category(db,id)
    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "content not found"
        )
    return category

@router.patch("/categories/{id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
def update(
    category_in:CategoryUpdate,
    id:UUID,
    db:Session=Depends(get_db),
    current_user:UserResponse=Depends(get_current_user)
    ):

    if current_user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You dont have authorization"
        )

    updated = update_category(db,id,category_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return updated

@router.patch("/categories/{id}/disable",status_code=status.HTTP_200_OK)
def disable(
    id:UUID,
    current_user:UserResponse=Depends(get_current_user),
    db:Session=Depends(get_db)
    ):

    if current_user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You dont have authorization"
        )

    disabled = disable_category(db,id)
    if not disabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return {"message" :"Category disabled" }


@router.patch("/categories/{id}/activate",status_code=status.HTTP_200_OK)
def activate_category(
    id:UUID,
    current_user:UserResponse=Depends(get_current_user),
    db:Session=Depends(get_db)
    ):

    if current_user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You dont have authorization"
        )

    activated= activate(db,id)
    if not activated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return "category activated"





