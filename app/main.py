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
app.include_router(checkout.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SwiftCommerce API - Speed and Scale!"}
