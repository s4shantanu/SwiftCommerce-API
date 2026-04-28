import json
from fastapi import APIRouter, Depends, HTTPException
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.config import settings
from app.models.user import User
from app.api.deps import get_current_user, get_db
from app.crud.product import get_products, create_product
from app.schemas.product import ProductOut, ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])

async def get_redis():
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield r
    finally:
        await r.aclose()

@router.get("/")
async def read_products(
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
):
    """
    Fetch products, with Redis caching integration.
    """
    cache_key = "products_list"
    cached_products = await redis_client.get(cache_key)
    
    if cached_products:
        return {"source": "redis_cache", "data": json.loads(cached_products)}
    
    db_products = await get_products(db)
    
    # Needs to be serialized to a dict for json.dumps
    serializable_products = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock, "category": p.category} for p in db_products]
    
    await redis_client.setex(cache_key, 60, json.dumps(serializable_products))
    
    return {"source": "database", "data": serializable_products}

@router.post("/", response_model=ProductOut)
async def create_new_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Requires auth to map out dummy inserts realistically
):
    """
    Create new product
    """
    return await create_product(db, product_in)
