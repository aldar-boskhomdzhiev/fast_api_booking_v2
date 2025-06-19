from fastapi import Query, APIRouter, Body

from src.repositories.rooms import RoomsRepository

from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение данных по всем номерам отеля")
async def get_rooms(hotel_id:int):

    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)




@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение данных по конкретному номеру")
async def get_rooms(hotel_id: int, room_id: int):

    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)



@router.delete("/{hotel_id/rooms/{room_id}", summary="Удаление данных")
async def delete_room(hotel_id: int, room_id: int):

    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status":"OK","room_id": room_id}


@router.post("{hotel_id}/rooms", summary="Добавление данных")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id,**room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
        return {"status": "OK", "data": room}


@router.put("/{hotel_id/rooms/{room_id}", summary="Обновление данных")
async def update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,id=room_id )
        await session.commit()
        return {"status": "OK"}



@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных")
async def partial_update_hotel(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).patch(_room_data, id=room_id, hotel_id=hotel_id,exclude_unset=True)
        await session.commit()
    return {"status": "OK"}

