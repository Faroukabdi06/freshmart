from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class CategoryCreate(BaseModel):
    name : str
    description : Optional[str] = None

class CategoryUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    is_active : Optional[bool] = None

class CategoryResponse(BaseModel):
    id : UUID
    name : str
    description : Optional[str] = None
    is_active : bool
    created_at : datetime

    class Config:
        from_attributes = True