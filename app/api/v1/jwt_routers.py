from fastapi import Depends, APIRouter
from auth.utils import TokenInfo, encode_jwt
from auth.auth import authenticate_user
from users.models import Users

router = APIRouter(prefix="/jwt", tags=["JWT"])


@router.post("/token", response_model=TokenInfo)
async def auth_issue_jwt(user: Users = Depends(authenticate_user)):
    payload = {"sub": user.username, "email": user.email}
    token = encode_jwt(payload=payload)
    return TokenInfo(access_token=token, token_type="Bearer")
