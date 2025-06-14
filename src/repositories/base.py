from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel



class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes= True )for model in result.scalars().all()]


    async def get_one(self, **filter_by):
        query = (select(self.model)
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes= True )


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes= True )

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()



    async def edit(self, data: BaseModel, **filter_by) -> None:
        edit_stmt = (
            update(self.model)
            .where(*[getattr(self.model, k) == v for k, v in filter_by.items()])
            .values(**data.model_dump())
        )
        await self.session.execute(edit_stmt)
        return None

    async def delete(self, **filter_by: object) -> None:

        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        records = result.scalars().all()

        if not records:
            raise HTTPException(status_code=404, detail="Object not found")
        elif len(records) > 1:
            raise HTTPException(status_code=404, detail="More than one object found")

        delete_stmt = delete(self.model).where(
            *[getattr(self.model, k) == v for k, v in filter_by.items()]
        )
        await self.session.execute(delete_stmt)

    async def patch(self, data: BaseModel, exclude_unset=False, **filter_by) -> None:
        update_stmt = (update(self.model)
                       .filter_by(**filter_by)
                       .values(**data.model_dump(exclude_unset= exclude_unset)))
        await self.session.execute(update_stmt)

