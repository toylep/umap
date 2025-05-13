from domain.models import MapPoint
from domain.repos.implementations import (
    BuildingPartRepo,
    RoomRepo,
    MapPointRepo,
    MapPointConnectionRepo,
)
from domain.dto import (
    BuildingPartDTO,
    RoomDTO,
    MapPointDTO,
    MapPointConnectionDTO,
    BuildingPartCreateDTO,
    RoomCreateDTO,
    MapPointCreateDTO,
)
from domain.services.base import AbstractService
import networkx as nx
# from sqlalc
class BuildingPartService(AbstractService[BuildingPartCreateDTO, BuildingPartDTO]):
    repo = BuildingPartRepo


class MapPointService(AbstractService[MapPointCreateDTO, MapPointDTO]):
    repo = MapPointRepo


class RoomService(AbstractService[RoomCreateDTO, RoomDTO]):
    repo = RoomRepo


class MapPointConnectionService(
    AbstractService[MapPointConnectionDTO, MapPointConnectionDTO]
):
    repo = MapPointConnectionRepo


    def path_to_svg_d(self,points: list) -> str:
        if not points:
            return ""

        # Формируем список координат в формате "x,y"
        coords = [f"{p.lng},{p.lat}" for p in points]

        # Добавляем префикс M для первой точки и L для остальных
        return f"M{coords[0]} " + " ".join(f"L{c}" for c in coords[1:])

    async def get_shortest_path(self, start_point_id: int, end_point_id: int):
        """Находит кратчайший путь между двумя точками по алгоритму Дейкстры."""
    
        # Создаем граф
        G = nx.Graph()
        map_point_repo = MapPointRepo()
        # Загружаем все точки
        points = await map_point_repo.get_all()
        for point in points:
            G.add_node(point.id, pos=(point.lng, point.lat))

        # Загружаем все соединения между точками
        connections = await self.repo().get_all()
        for conn in connections:
            print(conn)
            G.add_edge(conn.point_id_1, conn.point_id_2, weight=conn.distance)

        # Проверяем, существуют ли точки в графе
        if start_point_id not in G or end_point_id not in G:
            return None  # Нет пути

        # Ищем кратчайший путь
        try:
            path = nx.shortest_path(G, source=start_point_id, target=end_point_id, weight="weight")
            print(path)
            id_to_point = {point.id: point for point in points}
            sorted_path = [id_to_point[node] for node in path]
            path_str = self.path_to_svg_d(sorted_path)
            return {"data": path_str}
        except nx.NetworkXNoPath:
            return None  # Пути нет
