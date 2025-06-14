from fastapi import Query, APIRouter, Body

from src.repositories.hotels import HotelRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep

from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/{hotel_id}", summary="Получение одного отеля по id")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelRepository(session).get_one(id=hotel_id)


@router.get("", summary="Получение данных")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all(
            location = location,
            title = title,
            limit = per_page,
            offset = per_page * (pagination.page -1)
        )


@router.delete("/{hotel_id}", summary="Удаление данных")
async def delete_hotel(hotel_id: int):

    async with async_session_maker() as session:
        await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status":"OK","hotel_id": hotel_id}


@router.post("", summary="Добавление данных")
async def create_hotel(
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

        }
)):

    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()
        return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновление данных")
async def update_hotel(
    hotel_id: int,
    hotel_data: Hotel,
):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return {"status": "OK"}



@router.patch("/{hotel_id}", summary="Частичное обновление данных")
async def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelRepository(session).patch(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()
    return {"status": "OK"}

