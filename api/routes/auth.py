import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from ..database import get_db
from ..models import User, UserOut
from ..auth_utils import verify_google_token, create_token, get_current_user

router = APIRouter(tags=["auth"])


class GoogleAuthRequest(BaseModel):
    id_token: str


class AuthResponse(BaseModel):
    access_token: str
    user: UserOut


@router.post("/api/auth/google", response_model=AuthResponse)
async def google_auth(body: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    info = verify_google_token(body.id_token)
    google_sub = info.get("sub")
    if not google_sub:
        raise HTTPException(status_code=400, detail="Missing sub in Google token")

    result = await db.execute(select(User).where(User.google_sub == google_sub))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            id=str(uuid.uuid4()),
            google_sub=google_sub,
            email=info.get("email", ""),
            name=info.get("name", ""),
            avatar_url=info.get("picture"),
        )
        db.add(user)
    else:
        user.name = info.get("name", user.name)
        user.avatar_url = info.get("picture", user.avatar_url)

    await db.commit()
    await db.refresh(user)
    return AuthResponse(access_token=create_token(user.id), user=UserOut.model_validate(user))


@router.get("/api/me", response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return UserOut.model_validate(user)
