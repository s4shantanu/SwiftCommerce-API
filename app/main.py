from fastapi import FastAPI
from app.api import auth, products, checkout
from app.core.config import settings

# App initialization
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Register routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(checkout.router_checkout)
app.include_router(checkout.router_stripe)

@app.get("/")
def read_root():
    return {"message": "Welcome to SwiftCommerce API - Speed and Scale!"}


from app.db.session import engine
from app.db.base import Base # Ensure base import handles all models

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        # Ye line database mein tables create kar degi agar wo missing hain
        await conn.run_sync(Base.metadata.create_all)