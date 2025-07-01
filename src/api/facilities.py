from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAddRequest

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get("")
async def get_facilities(
        db:DBDep
):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(
        db:DBDep,
        title: FacilityAddRequest
):
    await db.facilities.add(title)
    await db.session.commit()
    return {'status': 'OK', 'facility': title}
