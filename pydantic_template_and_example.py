from sqlalchemy.orm import declarative_base, sessionmaker, Mapped
from sqlalchemy import Column, Integer, String, create_engine, select, insert, update, delete
from pydantic import BaseModel, ConfigDict
from sqlalchemy.testing.schema import mapped_column

Base = declarative_base()

class UserOrm(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()


class UserPydantic(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_user(user_id: int):
    with Session() as session:
        user = session.query(UserOrm).filter_by(id=user_id).one()

        if user:
            user_pydantic  = UserPydantic.model_validate(user)
            return user_pydantic.model_dump()


def add_user(user: UserPydantic):
    with Session() as session:
        stmt = insert(UserOrm).values(**user.model_dump())
        session.execute(stmt)
        session.commit()

def get_user_all():
    with Session() as session:
        query = select(UserOrm)
        res = session.execute(query)
        return res.scalars().all()




user_1 = UserPydantic(id=2,name='aldar', email='test@gmail.com')





#add_user(user_1)
#user_data = get_user(1)
#print(user_data)
res = get_user_all()

for item in res:
    print(UserPydantic.model_validate(item).model_dump())
    print(type(UserPydantic.model_validate(item).model_dump()))
    print(UserPydantic.model_validate(item), type(UserPydantic.model_validate(item)),sep='\n')



