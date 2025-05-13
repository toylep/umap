from sqlalchemy import Float, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()

class BuildingPart(Base):
    __tablename__ = "building_part"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)

    rooms = relationship("Room", back_populates="building_part")


class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    building_part_id: Mapped[int] = mapped_column(ForeignKey("building_part.id"))
    map_point_id: Mapped[int] = mapped_column(ForeignKey("map_point.id"),nullable=True)
    building_part = relationship("BuildingPart", back_populates="rooms")


class MapPoint(Base):
    __tablename__ = "map_point"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lng: Mapped[float] = mapped_column(Float)
    lat: Mapped[float] = mapped_column(Float)
    floor_num: Mapped[int] = mapped_column(Integer)
    
    # Связи между точками (двунаправленный граф)
    connections = relationship(
        "MapPointConnection",
        primaryjoin="or_(MapPoint.id == MapPointConnection.point_id_1, MapPoint.id == MapPointConnection.point_id_2)",
        back_populates="point",
    )


class MapPointConnection(Base):
    __tablename__ = "map_point_connections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    point_id_1: Mapped[int] = mapped_column(ForeignKey("map_point.id"))
    point_id_2: Mapped[int] = mapped_column(ForeignKey("map_point.id"))
    distance: Mapped[float] = mapped_column(Float, default=1)  # Дистанция между точками

    point = relationship(
        "MapPoint",
        primaryjoin="MapPoint.id == MapPointConnection.point_id_1",
        back_populates="connections",
        foreign_keys=[point_id_1],
    )