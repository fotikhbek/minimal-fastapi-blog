from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from database.user_dals import UserDAL
from users.models import Users
from auth.utils import validate_password, decode_jwt
from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer
from database.database import get_session
from fastapi.exceptions import HTTPException
from starlette import status


oath2_scheme = OAuth2PasswordBearer(tokenUrl='jwt/token')

async def _get_user_by_username_for_auth(username: str, db: AsyncSession= Depends(get_session)):
    async with db.begin():
        userdal = UserDAL(db)
        return await userdal.get_user_by_username(username=username)



async def authenticate_user(db: AsyncSession = Depends(get_session), username: str = Form(), password:str = Form()) -> Union[Users, None]:
    user = await _get_user_by_username_for_auth(username=username, db=db)
    if user is None:
        return
    if not validate_password(password=password, hashed_password=user.hashed_password):
        return
    return user


async def get_current_user(token: str = Depends(oath2_scheme), db: AsyncSession = Depends(get_session)):
    creditentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password'
    )
    payload = decode_jwt(token=token)
    username = payload.get('sub')
    if username is None:
        raise creditentials_exc
    user = await _get_user_by_username_for_auth(username=username, db=db)
    if user is None:
        raise creditentials_exc
    return user

