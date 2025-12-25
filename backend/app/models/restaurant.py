from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid

from app.db.base import Base

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String(20))
    working_hours = Column(JSON)




