from datetime import date

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            hotel_id: int | None = None,
    ):

        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
        #print(rooms_ids_to_get.compile(bind=engine,compile_kwargs={"literal_binds":True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))













