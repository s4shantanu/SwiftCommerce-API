from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from app.core.config import settings

# Humne 'bcrypt' select kiya hai jo ki bahut secure hai
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function 1: Password ko hash karne ke liye (Registration ke waqt)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function 2: Check karne ke liye ki login ke waqt dala gaya password sahi hai ya nahi
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt