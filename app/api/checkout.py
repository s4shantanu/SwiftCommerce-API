from fastapi import APIRouter, Depends, Request, HTTPException
import stripe
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.api.deps import get_current_user, get_db
from app.crud.product import get_product_by_id
from pydantic import BaseModel

# Create stripe webhook prefix if they specifically wanted it exposed on /stripe/webhook instead of /checkout
router_checkout = APIRouter(prefix="/checkout", tags=["Checkout"])
router_stripe = APIRouter(prefix="/stripe", tags=["Stripe"])

stripe.api_key = settings.STRIPE_API_KEY

class CheckoutItem(BaseModel):
    product_id: int
    quantity: int

@router_checkout.post("/")
async def create_checkout_session(
    item: CheckoutItem,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify product and prices from db instead of client passed values
    product = await get_product_by_id(db, product_id=item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price * 100), # stripe expects cents
                },
                'quantity': item.quantity,
            }],
            mode='payment',
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            customer_email=current_user.email,
            metadata={"product_id": product.id, "user_id": current_user.id}
        )
        return {"sessionId": session.id, "url": session.url}
    except Exception as e:
        return {"error": str(e)}

@router_stripe.post("/webhook", include_in_schema=False)
async def stripe_webhook(request: Request):
    """
    Stripe Webhooks endpoint /stripe/webhook
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return {"error": "Invalid payload"}
    except stripe.error.SignatureVerificationError as e:
        return {"error": "Invalid signature"}

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        product_id = session.get("metadata", {}).get("product_id")
        user_id = session.get("metadata", {}).get("user_id")
        
        # TODO: Decrease DB stock and mark order as verified
        pass

    return {"status": "success"}
