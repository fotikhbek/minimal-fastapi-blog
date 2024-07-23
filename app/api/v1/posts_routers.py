from fastapi import APIRouter, Depends, HTTPException
from database.database import get_session
from users.models import Users
from posts.schemas import PostScheme, DeletedPostScheme, UpdatedPostScheme
from api.v1.actions.post import (
    _create_post,
    _delete_post,
    _get_post_by_id,
    _get_all_posts,
    _get_user_posts,
    _update_post,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from auth.auth import get_current_user


router = APIRouter()


@router.get("/all")
async def get_all_posts(
    db: AsyncSession = Depends(get_session), user: Users = Depends(get_current_user)
):
    try:
        return await _get_all_posts(db=db)
    except IntegrityError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@router.get("/{post_id}")
async def get_post_by_id(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    user: Users = Depends(get_current_user),
) -> PostScheme:
    res = await _get_post_by_id(post_id=post_id, db=db)
    return PostScheme(header=res.header, content=res.constent, author=res.author)


@router.get("/my_posts")
async def get_current_users_posts(
    db: AsyncSession = Depends(get_session), user: Users = Depends(get_current_user)
):
    try:
        return await _get_user_posts(username=user.username, db=db)
    except IntegrityError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@router.post("/", response_model=PostScheme)
async def create_new_post(
    body: PostScheme,
    db: AsyncSession = Depends(get_session),
    user: Users = Depends(get_current_user),
):
    try:
        return await _create_post(
            title=body.header, content=body.content, author=user.username, db=db
        )
    except IntegrityError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@router.delete("/{post_id}", response_model=DeletedPostScheme)
async def delete_post(
    post_id: int,
    user: Users = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    post_to_delete = await _get_post_by_id(post_id=post_id, db=db)
    post_not_found_exc = HTTPException(status_code=404, detail="Post not found.")

    if not post_to_delete:
        raise post_not_found_exc

    if not user.username == post_to_delete.author:
        raise HTTPException(status_code=401, detail="Forbidden.")

    try:
        deleted_post = await _delete_post(post_id=post_id, db=db)
        return deleted_post
    except IntegrityError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@router.patch("/{body.id}")
async def update_post(
    body: UpdatedPostScheme,
    db: AsyncSession = Depends(get_session),
    user: Users = Depends(get_current_user),
):
    updated_post_params = body.model_dump(exclude_none=True)
    if updated_post_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter should be provided.",
        )
    post_to_update = await _get_post_by_id(post_id=updated_post_params["id"], db=db)
    if post_to_update is None:
        raise HTTPException(status_code=404, detail="Post not found.")

    if post_to_update.author != user.username:
        raise HTTPException(status_code=401, detail="Forbidden.")

    try:
        return await _update_post(body=updated_post_params, db=db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
