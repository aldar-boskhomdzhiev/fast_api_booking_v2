from fastapi import Query, APIRouter, Body

from src.repositories.hotels import HotelRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelResponse
from src.api.dependencies import PaginationDep

from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])


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
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Добавление данных")
async def create_hotel(
    hotel_data: Hotel = Body(
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
        hotel = await HotelRepository(session).add(hotel_data.model_dump())

    return {"status": "OK", "data": HotelResponse.model_validate(hotel)}


@router.put("/{hotel_id}", summary="Обновление данных")
def update_hotel(
    hotel_id: int,
    hotel_data: Hotel,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update(id=hotel_id, title=hotel_data.title, name=hotel_data.name)
            return {"status": "updated", "hotel": hotel}

    return {"status": "not_found"}, 404


@router.patch("/{hotel_id}", summary="Частичное обновление данных")
def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):

    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "updated", "hotel": hotel}
