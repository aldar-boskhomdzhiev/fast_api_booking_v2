from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

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
        return [self.schema.model_validate(model, from_attributes= True )for model in result.scalars().all()]

