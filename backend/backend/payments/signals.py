import logging
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from stream_chat import StreamChat

from .models import Payment

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Payment)
def sync_payment_status_with_stream_chat(sender, instance, created, **kwargs):
    # Only process if payment is succeeded and has an associated chat channel
    if instance.status == 'succeeded' and hasattr(instance, 'chat_channel') and instance.chat_channel:
        try:
            chat = instance.chat_channel

            # Check if there's a payment request message ID
            if not chat.payment_request_msg_id:
                logger.warning(f"Payment {instance.id} has no payment_request_msg_id in chat channel")
                return

            # Initialize Stream client
            client = StreamChat(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)

            # Update the message to mark it as paid
            updates = {
                'payment_status': 'paid',
                'payment_url': None,
            }

            client.update_message_partial(
                chat.payment_request_msg_id,
                {"set": updates},
                'gifthub'
            )

            logger.info(f"Updated payment message {chat.payment_request_msg_id} to paid status for payment {instance.id}")

        except Exception as e:
            logger.error(f"Failed to update payment message for payment {instance.id}: {str(e)}")
