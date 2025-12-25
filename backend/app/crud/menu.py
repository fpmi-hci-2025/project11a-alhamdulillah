from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.models.menu_item import MenuItem
from app.models.category import Category
from app.schemas.menu import MenuItemCreate, CategoryCreate

class CRUDMenuItem:
    def get(self, db: Session, id: UUID) -> Optional[MenuItem]:
        return db.query(MenuItem).filter(MenuItem.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        category_id: Optional[UUID] = None
    ) -> List[MenuItem]:
        query = db.query(MenuItem).filter(MenuItem.is_available == True)
        
        if category_id:
            query = query.filter(MenuItem.category_id == category_id)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: MenuItemCreate) -> MenuItem:
        db_obj = MenuItem(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDCategory:
    def get_multi(self, db: Session) -> List[Category]:
        return db.query(Category).all()
    
    def create(self, db: Session, obj_in: CategoryCreate) -> Category:
        db_obj = Category(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

menu_item = CRUDMenuItem()
category = CRUDCategory()




