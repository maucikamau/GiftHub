import stripe
import logging
from django.conf import settings
from django.contrib.auth.models import Permission
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Payment, StripeConnectedAccount

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    """
    Handle Stripe webhook events.
    This endpoint receives notifications about payment status changes.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    # Handle the event
    event_type = event['type']
    event_data = event['data']['object']

    logger.info(f"Received Stripe webhook event: {event_type}")

    # Handle payment intent events
    if event_type == 'payment_intent.succeeded':
        handle_payment_intent_succeeded(event_data)
    elif event_type == 'payment_intent.payment_failed':
        handle_payment_intent_failed(event_data)
    elif event_type == 'payment_intent.canceled':
        handle_payment_intent_canceled(event_data)

    # Handle account events
    elif event_type == 'account.updated':
        handle_account_updated(event_data)

    return JsonResponse({'status': 'success'})


def handle_payment_intent_succeeded(payment_intent):
    """Handle successful payment intent."""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
        payment.status = 'succeeded'
        payment.save()

        logger.info(f"Payment {payment.id} succeeded: {payment_intent['id']}")

        # You can add additional logic here, such as:
        # - Sending notification emails
        # - Updating campaign funding amounts
        # - Creating receipts

    except Payment.DoesNotExist:
        logger.warning(f"Payment not found for intent: {payment_intent['id']}")


def handle_payment_intent_failed(payment_intent):
    """Handle failed payment intent."""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
        payment.status = 'failed'
        payment.save()

        logger.warning(f"Payment {payment.id} failed: {payment_intent['id']}")

        # You can add additional logic here, such as:
        # - Sending notification to donor about failed payment

    except Payment.DoesNotExist:
        logger.warning(f"Payment not found for intent: {payment_intent['id']}")


def handle_payment_intent_canceled(payment_intent):
    """Handle canceled payment intent."""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
        payment.status = 'canceled'
        payment.save()

        logger.info(f"Payment {payment.id} canceled: {payment_intent['id']}")

    except Payment.DoesNotExist:
        logger.warning(f"Payment not found for intent: {payment_intent['id']}")


def handle_account_updated(account):
    """Handle updates to connected accounts."""
    try:
        connected_account = StripeConnectedAccount.objects.get(
            stripe_account_id=account['id']
        )

        # Update account capabilities
        connected_account.charges_enabled = account.get('charges_enabled', False)
        connected_account.payouts_enabled = account.get('payouts_enabled', False)
        connected_account.details_submitted = account.get('details_submitted', False)
        connected_account.save()

        # Grant payment permission if account is fully set up
        if connected_account.charges_enabled and connected_account.details_submitted:
            user = connected_account.user
            try:
                permission = Permission.objects.get(
                    content_type__app_label='payments',
                    codename='view_payment'
                )
                if not user.user_permissions.filter(id=permission.id).exists():
                    user.user_permissions.add(permission)
                    logger.info(f"Granted view_payment permission to user {user.id}")
            except Permission.DoesNotExist:
                logger.error("view_payment permission does not exist")

        logger.info(f"Updated connected account {connected_account.id}: {account['id']}")

    except StripeConnectedAccount.DoesNotExist:
        logger.warning(f"Connected account not found: {account['id']}")

