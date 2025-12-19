from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, Dict, Any

class RestaurantBase(BaseModel):
    name: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    working_hours: Optional[Dict[str, Any]] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantResponse(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID

