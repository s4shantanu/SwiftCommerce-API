from fastapi import APIRouter, Depends, Request
import stripe
from app.core.config import settings
from app.models.user import User
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/checkout", tags=["Checkout"])

# Stripe requires global API key set but we can also pass it in the API call
stripe.api_key = settings.STRIPE_API_KEY

class CheckoutItem(BaseModel):
    product_name: str
    amount: int  # in cents
    quantity: int

@router.post("/")
async def create_checkout_session(
    item: CheckoutItem,
    current_user: User = Depends(get_current_user)
):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product_name,
                    },
                    'unit_amount': item.amount,
                },
                'quantity': item.quantity,
            }],
            mode='payment',
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            customer_email=current_user.email
        )
        return {"sessionId": session.id, "url": session.url}
    except Exception as e:
        return {"error": str(e)}

@router.post("/webhook", include_in_schema=False)
async def stripe_webhook(request: Request):
    """
    Placeholder for handling Stripe Webhooks
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return {"error": "Invalid payload"}
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return {"error": "Invalid signature"}

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # TODO: Fulfill the purchase, update DB
        pass

    return {"status": "success"}
