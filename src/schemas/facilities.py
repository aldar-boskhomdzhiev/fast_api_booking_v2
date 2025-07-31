from pydantic import BaseModel


class FacilityAdd(BaseModel):
    title: str

class Facility(FacilityAdd):
    id: int

class RoomFacilityAdd(BaseModel):
    rooms_id: int
    facilities_id: int

class RoomFacility(RoomFacilityAdd):
    id: int
    