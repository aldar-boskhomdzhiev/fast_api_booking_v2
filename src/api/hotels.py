from datetime import date

from fastapi import Query, APIRouter, Body

from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/{hotel_id}", summary="Получение одного отеля по id")
async def get_hotel(hotel_id: int, db: DBDep):
        return await db.hotels.get_one_or_none(id=hotel_id)


@router.get("", summary="Получение данных")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация отеля"),
    date_from: date = Query(example="2025-10-01"),
    date_to: date = Query(example="2025-10-10"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page-1),
        )


@router.delete("/{hotel_id}", summary="Удаление данных")
async def delete_hotel(hotel_id: int, db: DBDep):

    await db.hotels.delete(id=hotel_id)
    await db.session.commit()
    return {"status":"OK","hotel_id": hotel_id}


@router.post("", summary="Добавление данных")
async def create_hotel(
    db:DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "Пример отеля": {
                "summary": "Пример 5-звёздочного отеля",
                "value": {
                    "title": "Отель у моря 5 звезд",
                    "location": "sochi_y_moray"
                }
            },
            "Пример отеля 2": {
                "summary": "Пример 5-звёздочного отеля ДУБАЙ",
                "value": {
                    "title": "Отель в Дубае 5 звезд",
                    "location": "ДУБАЙ-МОЛ"
                }
            },

        }),
):
    await db.hotels.add(hotel_data)
    await db.session.commit()
    return {"status": "OK", "data": hotel_data}


@router.put("/{hotel_id}", summary="Обновление данных")
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.session.commit()
    return {"status": "OK"}



@router.patch("/{hotel_id}", summary="Частичное обновление данных")
async def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep,
):

    await db.hotels.patch(hotel_data, id=hotel_id, exclude_unset=True)
    await db.session.commit()
    return {"status": "OK"}

