from posts.schemas import PostScheme, DeletedPostScheme
from database.post_dals import PostDAL
from typing import Union, List
from posts.models import Posts


async def _create_post(title, content, author, db) -> PostScheme:
    async with db.begin():
        post_dal = PostDAL(db_session=db)
        await post_dal.create_post(title=title, content=content, author=author)

    return PostScheme(header=title, content=content, author=author)


async def _delete_post(post_id, db) -> DeletedPostScheme:
    async with db.begin():
        post_dal = PostDAL(db_session=db)
        await post_dal.delete_post(post_id=post_id)
    return DeletedPostScheme(post_id=post_id)


async def _get_post_by_id(post_id, db) -> PostScheme:
    async with db.begin():
        post_dal = PostDAL(db_session=db)
        post = await post_dal.get_post_by_id(post_id=post_id)
    if post:
        return PostScheme(header=post.header, content=post.content, author=post.author)


async def _get_user_posts(username, db) -> Union[List[Posts], None]:
    async with db.begin():
        post_dal = PostDAL(db_session=db)
        result = await post_dal.get_all_user_posts(username=username)
        if result:
            return result


async def _get_all_posts(db) -> Union[List[Posts], None]:
    async with db.begin():
        post_dal = PostDAL(db_session=db)
        return await post_dal.get_all_posts()


async def _update_post(body: dict, db) -> Union[Posts, None]:
    async with db.begin():
        post_dal = PostDAL(db_session=db)
        return await post_dal.update_post(body)
