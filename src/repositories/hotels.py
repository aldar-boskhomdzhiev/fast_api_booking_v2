from sqlalchemy import select, func

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):

        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location.strip()}%"))

        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title.strip()}%"))

        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        print("location:", location)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        return result.scalars().all()

