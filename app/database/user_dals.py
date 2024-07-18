from typing import Union

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import Users

class UserDAL:
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        username: str,
        email: str,
        hashed_password: str
    ) -> Users:
        new_user = Users(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


    async def delete_user(self, username) -> Union[id, None]:
        query = (
            update(Users)
            .where(and_(Users.username == username, Users.is_active == True))
            .values(is_active=False)
            .returning(Users.id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def _get_user_by_id(self, id) -> Union[Users, None]:
        query = select(Users).where(Users.id == id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
    
    
    async def get_user_by_username(self, username: str) -> Union[Users, None]:
        query = select(Users).where(Users.username == username)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, id, **kwargs) -> Union[id, None]:
        query = (
            update(Users)
            .where(and_(Users.id == id, Users.is_active == True))
            .values(kwargs)
            .returning(Users.id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    