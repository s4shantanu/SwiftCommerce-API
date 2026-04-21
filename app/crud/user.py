from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def create_user(db: AsyncSession, user: UserCreate):
    # 1. Password ko hash karo
    hashed_pwd = get_password_hash(user.password)
    
    # 2. Database model instance banao
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pwd
    )
    
    # 3. DB mein save karo
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user