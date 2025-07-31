from datetime import date

from fastapi import Query, APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение данных по всем номерам отеля")
async def get_rooms(
        hotel_id:int,
        db:DBDep,
        date_from: date = Query(example="2025-10-01"),
        date_to: date = Query(example="2025-10-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение данных по конкретному номеру")
async def get_rooms(hotel_id: int, room_id: int, db:DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)



@router.delete("/{hotel_id/rooms/{room_id}", summary="Удаление данных")
async def delete_room(hotel_id: int, room_id: int, db:DBDep):

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.session.commit()
    return {"status":"OK","room_id": room_id}


@router.post("{hotel_id}/rooms", summary="Добавление данных")
async def create_room(db:DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id,**room_data.model_dump())
    room = await db.rooms.add(_room_data)


    rooms_facilities_data = [RoomFacilityAdd(rooms_id=room.id, facilities_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id/rooms/{room_id}", summary="Обновление данных")
async def update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
    db:DBDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data,id=room_id )
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.session.commit()
    return {"status": "OK"}



@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных")
async def partial_update_hotel(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db:DBDep,
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.patch(_room_data, id=room_id, hotel_id=hotel_id,exclude_unset=True)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.session.commit()
    return {"status": "OK"}

