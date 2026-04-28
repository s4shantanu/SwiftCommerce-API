from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.schemas.token import TokenPayload
from app.crud.user import get_user_by_email

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise HTTPException(status_code=403, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = await get_user_by_email(db, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user