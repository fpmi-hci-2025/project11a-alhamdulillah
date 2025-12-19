from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.base import get_db
from app.crud import restaurant as crud_restaurant
from app.schemas.restaurant import RestaurantResponse

router = APIRouter()

@router.get("/restaurants", response_model=List[RestaurantResponse])
def get_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    restaurants = crud_restaurant.restaurant.get_multi(db, skip=skip, limit=limit)
    return restaurants

@router.get("/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(
    restaurant_id: UUID,
    db: Session = Depends(get_db)
):
    restaurant = crud_restaurant.restaurant.get(db, id=restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

