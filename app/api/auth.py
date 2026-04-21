# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
async def register_user(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Check karo ki user pehle se to exist nahi karta
    # (Abhi ke liye hum direct create kar rahe hain, baad mein check logic dalenge)
    
    new_user = await create_user(db=db, user=user_in)
    return new_user