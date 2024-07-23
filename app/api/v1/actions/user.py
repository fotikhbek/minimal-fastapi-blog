from typing import Union
from users.schemas import ShowUser, CreateUser
from database.user_dals import UserDAL
from users.models import Users
from auth.utils import hash_password


async def _create_new_user(body: CreateUser, db) -> ShowUser:
    async with db.begin():
        userdal = UserDAL(db)
        await userdal.create_user(
            username=body.username,
            email=body.email,
            hashed_password=hash_password(body.password),
        )

    return ShowUser(username=body.username, email=body.email, is_active=True)


async def _delete_user(username, db) -> Union[id, None]:
    async with db.begin():
        user_dal = UserDAL(db)
        deleted_user_id = await user_dal.delete_user(username=username)
        return deleted_user_id


async def _get_user_by_username(username: str, db) -> Union[Users, None]:
    async with db.begin():
        userdal = UserDAL(db)
        user = await userdal.get_user_by_username(username=username)
        if user is not None:
            return user


async def _update_user(updated_user_params: dict, id, db) -> Union[id, None]:
    async with db.begin():
        userdal = UserDAL(db)
        updated_user_id = await userdal.update_user(updated_user_params, id=id)
        return updated_user_id
