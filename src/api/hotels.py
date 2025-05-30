from fastapi import Query, APIRouter


from src.schemas.hotels import Hotel
from src.api.dependencies import PaginationDep


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Paris", "name": "paris"},
    {"id": 4, "title": "New York", "name": "new_york"},
    {"id": 5, "title": "Tokyo", "name": "tokyo"},
    {"id": 6, "title": "Berlin", "name": "berlin"},
    {"id": 7, "title": "Rome", "name": "rome"},
    {"id": 8, "title": "Barcelona", "name": "barcelona"},
    {"id": 9, "title": "Bangkok", "name": "bangkok"},
    {"id": 10, "title": "Sydney", "name": "sydney"},
]



router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",summary='Получение данных')
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="ID отеля"),
    title: str | None = Query(None, description="Название отеля"),

):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page*(pagination.page-1):][:pagination.per_page]
    return hotels_



@router.delete("/{hotel_id}",summary='Удаление данных')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("",summary='Добавление данных')
def create_hotel(
        hotel_data: Hotel
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
        }
    )

    return {"status": "OK"}


@router.put("/{hotel_id}", summary='Обновление данных')
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


@router.patch("/{hotel_id}",summary='Частичное обновление данных')
def partial_update_hotel(
    hotel_id: int,
    hotel_data: Hotel,
):

    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "updated", "hotel": hotel}
