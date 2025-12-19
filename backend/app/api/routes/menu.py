from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.base import get_db
from app.crud import menu as crud_menu
from app.schemas.menu import MenuItemResponse, CategoryResponse

router = APIRouter()

@router.get("/menu", response_model=List[MenuItemResponse])
def get_menu(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    items = crud_menu.menu_item.get_multi(
        db, 
        skip=skip, 
        limit=limit,
        category_id=category_id
    )
    return items

@router.get("/menu/{item_id}", response_model=MenuItemResponse)
def get_menu_item(
    item_id: UUID,
    db: Session = Depends(get_db)
):
    item = crud_menu.menu_item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = crud_menu.category.get_multi(db)
    return categories

