from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class HotelRepository(BaseRepository):
    model = RoomsOrm
