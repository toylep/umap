from domain.models import Room, BuildingPart
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.db import AsyncSessionLocal
from domain.dto import (
    RoomDTO,
    BuildingPartDTO,
    RoomCreateDTO,
    BuildingPartCreateDTO,
    MapPointDTO,
    MapPointCreateDTO,
    MapPointConnectionDTO,
    MapPointConnectionCreateDTO,
)
from sqlalchemy.future import select
from domain.services.implementations import (
    MapPointConnectionService,
    RoomService,
    BuildingPartService,
    MapPointService,
)
from domain.repos.implementations import (
    MapPointRepo,
    MapPointConnectionRepo,
    RoomRepo,
    BuildingPartRepo,
)
from typing import List
router = APIRouter()


@router.get("/rooms", response_model=List[RoomDTO])
async def get_rooms():
    return await RoomService().get_all()


@router.post("/rooms", response_model=RoomDTO)
async def add_room(dto: RoomCreateDTO):
    return await RoomService().add(dto)


@router.get("/building_parts", response_model=List[BuildingPartDTO])
async def get_building_parts():
    return await BuildingPartService().get_all()


@router.post("/building_parts", response_model=BuildingPartDTO)
async def add_building_part(dto: BuildingPartCreateDTO):
    # result = 
    return await BuildingPartService().add(dto)


@router.get("/map_points", response_model=List[MapPointDTO])
async def get_map_points():
    return await MapPointService().get_all()


@router.post("/map_points", response_model=MapPointDTO)
async def add_map_point(dto: MapPointCreateDTO):
    return await MapPointService().add(dto)


@router.get("/map_point_connections", response_model=List[MapPointConnectionDTO])
async def get_map_point_connections():
    return await MapPointService().get_all()


@router.post("/map_point_connections", response_model=MapPointConnectionDTO)
async def add_map_point_connection(dto: MapPointConnectionCreateDTO):
    return await MapPointService().add(dto)

@router.get("/shortest_path")
async def get_shortest_path(start_id: int, end_id: int):
    return await MapPointConnectionService().get_shortest_path(start_id, end_id)