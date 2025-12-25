from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate

class CRUDRestaurant:
    def get(self, db: Session, id: UUID) -> Optional[Restaurant]:
        return db.query(Restaurant).filter(Restaurant.id == id).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Restaurant]:
        return db.query(Restaurant).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: RestaurantCreate) -> Restaurant:
        db_obj = Restaurant(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

restaurant = CRUDRestaurant()




