# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_new_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if user exists
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists."
        )
    
    # 2. Create user
    return await create_new_user(db=db, user=user_in)