from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id, price=room_price, **booking_data.model_dump(exclude_unset=True)
    )
    booking = await db.booking.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(
    db: DBDep,
):
    return await db.booking.get_all()


@router.get("/bookings/me")
async def get_bookings_me(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.booking.get_one(user_id=user_id)
