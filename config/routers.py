from fastapi import APIRouter
from domain.controllers import router as main_router

# from domain.routes.implementations import room_router


base_router = APIRouter(prefix="/api")
base_router.include_router(main_router)
