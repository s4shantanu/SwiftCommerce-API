# app/core/security.py
from passlib.context import CryptContext

# Humne 'bcrypt' select kiya hai jo ki bahut secure hai
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function 1: Password ko hash karne ke liye (Registration ke waqt)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function 2: Check karne ke liye ki login ke waqt dala gaya password sahi hai ya nahi
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
    