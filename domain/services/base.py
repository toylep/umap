from typing import TypeVar, Generic
from pydantic import BaseModel

CreateDTO = TypeVar("CreateDTO")
DTO = TypeVar("DTO", bound=BaseModel)


class AbstractService(Generic[CreateDTO, DTO]):
    repo = None

    async def get_all(self):
        return await self.repo().get_all()

    async def get_by_id(self, item_id: int):
        return await self.repo().get_by_id(item_id)

    async def add(self, dto: CreateDTO):
        return await self.repo().add(dto.model_dump())

    async def update(self, item_id: int, dto: CreateDTO):
        return await self.repo().update(item_id, dto.model_dump())

    async def delete(self, item_id: int):
        return DTO.model(**(await self.repo().delete(item_id)))
