# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Database ka address (URL)
# Format: postgresql+asyncpg://<username>:<password>@<host>:<port>/<db_name>
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:yourpassword@localhost/swiftcommerce"

# 2. Engine: Ye asli connector hai jo connection handle karta hai
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 3. Session: Ye wo 'baatchit' hai jo hum har request par kholenge
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# 4. Base: Isse hum apne tables (Models) banayenge
Base = declarative_base()