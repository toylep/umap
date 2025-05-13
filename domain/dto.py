from typing import List, Optional
from pydantic import BaseModel


# 🔹 Базовая модель
class CustomModel(BaseModel):
    id: Optional[int] = None

    class Config:
        from_attributes = True


# 🔹 DTO для BuildingPart
class BuildingPartDTO(CustomModel):
    name: str


# 🔹 DTO для Room
class RoomDTO(CustomModel):
    name: str
    building_part_id: int
    map_point_id: Optional[int]

# 🔹 DTO для MapPoint
class MapPointDTO(CustomModel):
    lng: float
    lat: float
    floor_num: int



# 🔹 DTO для связи точек (MapPointConnection)
class MapPointConnectionDTO(CustomModel):
    point_id_1: int
    point_id_2: int
    distance: float = 1  # Дистанция между точками


# -----------------------------


# 🔹 DTO для создания BuildingPart
class BuildingPartCreateDTO(BaseModel):
    name: str


# 🔹 DTO для создания Room
class RoomCreateDTO(BaseModel):
    name: str
    building_part_id: int  # ID части здания, к которой относится комната


# 🔹 DTO для создания MapPoint
class MapPointCreateDTO(BaseModel):
    lng: float
    lat: float
    floor_num: int
    
    
# 🔹 DTO для создания связи между точками (MapPointConnection)
class MapPointConnectionCreateDTO(BaseModel):
    point_id_1: int
    point_id_2: int
    distance: float = 1  # Дистанция между точками (по умолчанию 1)
