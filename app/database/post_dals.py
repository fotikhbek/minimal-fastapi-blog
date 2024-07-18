from typing import Union, List
from sqlalchemy import and_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from posts.models import Posts

class PostDAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_post(self, title: str, content: str, author: str) -> Posts:
        post = Posts(header=title, content=content, author = author)
        self.db_session.add(post)
        await self.db_session.commit()
        return post

    async def get_post_by_id(self, post_id) ->Union[Posts, None]:
        stmt = select(Posts).where(Posts.id == post_id)
        res = await self.db_session.execute(stmt)
        post_row = res.fetchone()
        if post_row is not None:
            return post_row[0]

    async def get_all_user_posts(self, username) -> Union[List[Posts], None]:
        stmt = select(Posts).where(Posts.author==username)
        res = await self.db_session.execute(stmt)
        return res.mappings().all()

    async def get_all_posts(self) -> Union[List[Posts], None]:
        res = await self.db_session.execute(select(Posts))
        return res.mappings().all()

    async def delete_post(self, post_id) -> int:
        stmt = (delete(Posts).where(Posts.id == post_id))
        await self.db_session.execute(stmt)
        return post_id

    async def update_post(self,body: dict) -> Union[Posts, None]:
        stmt = (update(Posts).where(Posts.id == body['id'])
                .values(body).returning(Posts.id))
        res = await self.db_session.execute(stmt)
        return res.mappings().all()