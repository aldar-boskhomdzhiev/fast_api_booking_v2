from fastapi import APIRouter, HTTPException, Response

from sqlalchemy.exc import IntegrityError

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):

    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='Пользователь с таким email не зарегистрирован')
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Пароль неверный')
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return {"access_token": access_token}


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            user = await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {"status": "OK", "data": user}
        except IntegrityError:
            raise HTTPException(
                status_code=409, detail="Такой пользователь уже существует"
            )


@router.get("/me")
async def get_me(
        user_id: UserIdDep,
):
     async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
     return {"user": user}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out"}