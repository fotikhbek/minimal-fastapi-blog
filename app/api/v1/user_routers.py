from fastapi import APIRouter, Depends, HTTPException
from database.database import get_session
from users.models import Users
from users.schemas import ShowUser, CreateUser, DeleteUserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.actions.user import _create_new_user, _delete_user, _get_user_by_username
from sqlalchemy.exc import IntegrityError
from auth.auth import get_current_user


router = APIRouter()


@router.post("/register/", response_model=ShowUser)
async def register_user(
    body: CreateUser, db: AsyncSession = Depends(get_session)
) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.get("/{username}", response_model=ShowUser)
async def get_user_by_username(
    username: str,
    db: AsyncSession = Depends(get_session),
    current_user: Users = Depends(get_current_user),
) -> ShowUser:
    user = await _get_user_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="{username} not found.")
    return user


@router.get("/me", response_model=ShowUser)
async def get_current_user_from_token(current_user: Users = Depends(get_current_user)):
    return ShowUser(
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
    )


@router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    username: str,
    db: AsyncSession = Depends(get_session),
    user: Users = Depends(get_current_user),
) -> DeleteUserResponse:
    user_not_found_exc = HTTPException(status_code=404, detail="{username} not found.")

    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden.")

    user_to_delete = await get_user_by_username(username=username, db=db)

    if user_to_delete is None:
        raise user_not_found_exc

    deleted_user = await _delete_user(username=user_to_delete.username)
    if deleted_user is None:
        raise user_not_found_exc
    return DeleteUserResponse(deleted_user=deleted_user)
