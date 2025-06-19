from datetime import datetime

from pydantic import BaseModel


class BookingsAddRequest(BaseModel):
    date_from: datetime
    date_to: datetime
    price: int


class BookingsAdd(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: datetime
    date_to: datetime
    price: int


class Bookings(BookingsAdd):
    id: int
    room_id: int
    user_id: int

class BookingsPatchRequest(BaseModel):
    date_from: datetime
    date_to: datetime
    price: int


class BookingsPatch(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: datetime
    date_to: datetime
    price: int



