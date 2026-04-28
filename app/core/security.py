# app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt



# JWT Settings (Ideally should be in config.py)
SECRET_KEY = "your-secret-key-change-this" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
    

# JWT Settings (Ideally should be in config.py)
SECRET_KEY = "your-secret-key-change-this" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)