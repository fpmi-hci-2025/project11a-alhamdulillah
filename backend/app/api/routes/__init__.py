from fastapi import APIRouter
from app.api.routes import menu, restaurant

api_router = APIRouter()

api_router.include_router(menu.router, tags=["menu"])
api_router.include_router(restaurant.router, tags=["restaurants"])




