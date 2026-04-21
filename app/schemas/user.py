from pydantic import BaseModel, EmailStr


# Jab user register karega, ye data humein chahiye
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

# Jab hum user ka data wapas bhejenge (Response), tab password nahi bhejenge!
class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True # Ye SQLAlchemy model ko Pydantic mein convert karne ke liye hai