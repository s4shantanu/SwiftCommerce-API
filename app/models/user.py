from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base # Jo humne pehle discuss kiya tha

class User(Base):
    __tablename__ = "users" # Database mein table ka naam

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False) # Admin banne ke liye