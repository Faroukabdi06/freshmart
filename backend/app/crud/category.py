from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional,List

from app.models.category import Category
from app.schemas.category import CategoryCreate,CategoryUpdate


def create_category(db:Session, category_in:CategoryCreate)->Category:
    category = Category(
        name = category_in.name,
        description = category_in.description
    )

    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_all_categories(db:Session)->List[Category]:
    return db.query(Category).filter(Category.is_active==True).all()

def get_all_categories_admin(db:Session)->List[Category]:
    return db.query(Category).all()

def get_category(db:Session, category_id:UUID)->Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db:Session, category_name:str):
    return db.query(Category).filter(Category.name == category_name).first()

def update_category(db:Session, category_id:UUID, update:CategoryUpdate):
    category = get_category(db,category_id)
    if not category:
        return None

    if update.name is not None:
        category.name = update.name

    if update.description is not None:
        category.description = update.description

    if update.is_active is not None:
        category.is_active = update.is_active

    db.commit()
    db.refresh(category)

    return category

def disable_category(db:Session, category_id:UUID):
    category =get_category(db,category_id)
    if not category:
        return None

    category.is_active = False
    db.commit()
    db.refresh(category)
    return category

def activate(db:Session,category_id:UUID):
    category =get_category(db,category_id)
    if not category:
        return None

    category.is_active = True
    db.commit()
    db.refresh(category)
    return category

