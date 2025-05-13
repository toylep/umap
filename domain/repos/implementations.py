from domain.models import BuildingPart, Room, MapPoint, MapPointConnection
from domain.repos.base import SQLRepo


class BuildingPartRepo(SQLRepo):
    model_cls = BuildingPart


class RoomRepo(SQLRepo):
    model_cls = Room


class MapPointRepo(SQLRepo):
    model_cls = MapPoint


class MapPointConnectionRepo(SQLRepo):
    model_cls = MapPointConnection
