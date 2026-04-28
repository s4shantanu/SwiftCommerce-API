import json
from fastapi import APIRouter, Depends
import redis.asyncio as redis
from app.core.config import settings
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

# Dependency to get redis connection
async def get_redis():
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield r
    finally:
        await r.aclose()

@router.get("/")
async def get_products(
    redis_client: redis.Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch products, with Redis caching integration.
    """
    cache_key = "products_list"
    cached_products = await redis_client.get(cache_key)
    
    if cached_products:
        return {"source": "redis_cache", "data": json.loads(cached_products)}
    
    # Simulate DB fetch
    db_products = [
        {"id": 1, "name": "Wireless Headphones", "price": 99.99},
        {"id": 2, "name": "Mechanical Keyboard", "price": 129.50},
        {"id": 3, "name": "Gaming Mouse", "price": 59.99},
    ]
    
    # Set in cache for 60 seconds
    await redis_client.setex(cache_key, 60, json.dumps(db_products))
    
    return {"source": "database", "data": db_products}
