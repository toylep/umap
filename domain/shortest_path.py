import heapq
from typing import List, Tuple
from config.db import AsyncSessionLocal
from domain.models import MapPoint, MapPointConnection, Room
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_shortest_path(
    start_room_id: int, end_room_id: int
) -> List[Tuple[float, float]]:
    """
    Находит кратчайший путь между двумя комнатами по карте (асинхронно).

    :param db: Асинхронная сессия SQLAlchemy
    :param start_room_id: ID начальной комнаты
    :param end_room_id: ID конечной комнаты
    :return: список координат [(lng, lat), ...] кратчайшего пути
    """
    with AsyncSessionLocal() as db:
        # Получаем начальную и конечную комнаты
        start_room = await db.get(Room, start_room_id)
        end_room = await db.get(Room, end_room_id)

        if not start_room or not end_room:
            raise ValueError("Одна из комнат не найдена")

        start_point = start_room.map_point
        end_point = end_room.map_point

        # Запрос всех соединений между точками
        result = await db.execute(select(MapPointConnection))
        connections = result.scalars().all()

        # Строим граф
        graph = {}
        for conn in connections:
            if conn.point_id_1 not in graph:
                graph[conn.point_id_1] = []
            if conn.point_id_2 not in graph:
                graph[conn.point_id_2] = []

            graph[conn.point_id_1].append((conn.distance, conn.point_id_2))
            graph[conn.point_id_2].append(
                (conn.distance, conn.point_id_1)
            )  # Двунаправленная связь

        # Алгоритм Dijkstra
        pq = [(0, start_point.id)]  # Очередь (расстояние, id точки)
        distances = {start_point.id: 0}
        previous = {start_point.id: None}

        while pq:
            current_dist, current_id = heapq.heappop(pq)

            if current_id == end_point.id:
                break

            for neighbor_dist, neighbor_id in graph.get(current_id, []):
                new_dist = current_dist + neighbor_dist
                if new_dist < distances.get(neighbor_id, float("inf")):
                    distances[neighbor_id] = new_dist
                    previous[neighbor_id] = current_id
                    heapq.heappush(pq, (new_dist, neighbor_id))

        # Восстанавливаем путь
        path = []
        node = end_point.id
        while node is not None:
            result = await db.execute(select(MapPoint).where(MapPoint.id == node))
            point = result.scalar_one_or_none()
            if point:
                path.append((point.lng, point.lat))
            node = previous.get(node)

        return path[::-1]  # Разворачиваем путь от с
